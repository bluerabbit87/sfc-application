'''
Created on Dec 6, 2015

@author: root
'''
import json
import pprint


class descriptorManager(object):
    '''
    classdocs
    '''




    def __init__(self, logger):
        '''
        Constructor
        '''
        self.__logger = logger
    
    def parse_arg_options(self, additional_options_enabled, additional_options_length, args):
        self.__logger.debug("args %s" % args)
        options = {}
        
        if additional_options_enabled:
            if (len(args) != 1) and (len(args) % additional_options_length == 1):
                for i in range (1, len(args) / additional_options_length):
                    option = []
                    for j in range (0, additional_options_enabled):
                        option.append(args[i * 3 + j])
                    options.append(args[i])

        self.__logger.debug(options) 
        return options

    def create_entry(self, json_data=None, name=None, sf_list=None):
        print "create tenant [ex: firewall, NAT, DPI]"   
       
        entry = {}
        
        if json_data != None:
            entry = json_data
            
        else:
            if name == None:
                entry ["name"] = raw_input("please input the name of the tenant  [ex: custumer A, custumer B] : ")
            else:
                entry ["name"] = name
            

            if sf_list == None:    
                sf_list = []
                entry ["sf_list"] = sf_list
                      
                try:
                    while True:
                        sf_list.append(raw_input ("please input the name of the of SF (SFs: %s) (exit: ctrl + c) : " % (sf_list)))
                        
                except KeyboardInterrupt:
                    print ""
                    
            else:
                entry ["sf_list"] = sf_list
        
         
        result = self.validate_entry(entry) 
        if result == -1:
            return 0
        
        cursor = self.__DBcollection.find({"name": entry ["name"]})
        count = cursor.count()
        
        if count > 0:
            print "already, the service function is exist" 
            return -1
        
        with open('result.json', 'w') as fp:
            json.dump(entry, fp)
        
        
        self.__DBcollection.insert(entry)
        pprint.pprint(entry)
        print "The service function insertion is completed" 
        
    
    def validate_entry(self, enty):
        print enty
        
        if enty ["name"] != "":
            print "name is OK"
        else: 
            print "error"
            return -1
        

        if enty["sf_list"] != None:    
            for value in enty["sf_list"]:
                print value
#                 if value["name"] != "":
#                     print "name is OK"
#                 else:
#                     return -1
#                 

        return 0

    def list_entry(self):
        print "list entries of the service function forwarder"
        cursor = self.__DBcollection.find()
        list = cursor[:]
        
        print "%s %s %s" % ("id".ljust(25), "name".ljust(15), "sf list".ljust(30))
        
        for document in list:
            print "%s" % str(document["_id"]).ljust(25),
            print "%s" % document["name"].ljust(15),
            print "%s" % str(document["sf_list"]).ljust(30),
            print ""
            
        return list
        
    
    def update_entry(self, json_data=None, name=None, sf_list=None):
        print "update-sf"    
        
        # sfc_db.service_functions.find({"name": name})
        entry_name = "" 
        
        if json_data:
            exist = self.__DBcollection.find({"name": json_data["name"]}).count()
            entry_name = json_data["name"]
        elif name:
            exist = self.__DBcollection.find({"name": name}).count()
            entry_name = name
        else:
            return -1 
        
        print "%s exist %s" % (entry_name, exist)
        
        
        if exist:
            self.delete_entry(entry_name)
            self.create_entry(json_data=json_data, name=entry_name, sf_list=sf_list)
            print "update success"    
 
        else:
            print "update fail, there is no inputed sf entry"    
          

    def delete_entry(self, name="all"):
        print "delete the service function entrie"
        if name == "all":
            result = self.__DBcollection.remove()
        else:
            result = self.__DBcollection.remove({"name": name})
            
        print "%s entries are deleted" % result['n']
