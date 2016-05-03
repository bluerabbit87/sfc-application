'''
Created on Nov 30, 2015

@author: root
'''
"""'VNFFG_list_7': {'name': 'VNFFG_list_7', 'sf_list': ['Endian A', 'Endian B']}"""
            
import json
import pprint


class VNFFGManager(object):
    '''
    classdocs
    '''


    def __init__(self, sfc_db_, logger_):
        '''
        Constructor
        '''
        self.__DBcollection = sfc_db_.VNF_forwarding_graph
        self.__logger = logger_
    
    def parse_args(self, opts_enabled, args):
        print "args %s" % args
        options = []
        if opts_enabled:
            for i in range (1, len(args)):
                print args[i]
                options.append(args[i])
                    
        pprint.pprint(options) 
        return options

    def create_entry(self, json_data=None, name=None, sf_list=None):
        self.__logger.info("create VNFFG [ex: firewall, NAT, DPI]")
        
        entry = {}
        
        if json_data != None:
            entry = json_data
            
        else:
            if name == None:
                entry ["name"] = raw_input("please input the name of the tenant  [ex: custumer A, custumer B] : ")
            else:
                self.__logger.debug("name is empty")
                exit
                
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
            self.__logger.error("already, the VNFFG is exist")
            return -1
        
        with open('result.json', 'w') as fp:
            json.dump(entry, fp)
        
        
        self.__DBcollection.insert(entry)
        self.__logger.debug(entry)
        self.__logger.info("The service function insertion is completed")
    
    def validate_entry(self, enty):
        print enty
        
        if enty ["name"] != "":
            self.__logger.debug("name is OK")
        else: 
            self.__logger.error("name is empty")
            return -1
        

        if enty["sf_list"] != None:    
            for value in enty["sf_list"]:
                print value

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
        self.__logger.info("update end point")
        
        entry_name = "" 
        
        if json_data:
            exist = self.__DBcollection.find({"name": json_data["name"]}).count()
            entry_name = json_data["name"]
        elif name:
            exist = self.__DBcollection.find({"name": name}).count()
            entry_name = name
        else:
            return -1 
        
        self.__logger.debug("%s exist %s" % (entry_name, exist))
        
        
        if exist:
            self.delete_entry(entry_name)
            self.create_entry(json_data=json_data, name=entry_name, sf_list=sf_list)
            self.__logger.debug("update success")
        
        else:
            self.__logger.error("update fail, there is no inputed sf entry")
          

    def delete_entry(self, name="all"):
        self.__logger.info("delete the end point entrie")
        if name == "all":
            result = self.__DBcollection.remove()
        else:
            result = self.__DBcollection.remove({"name": name})
        
        self.__logger.info("%s entries are deleted" % result['n'])
