'''
Created on Nov 30, 2015

@author: root
'''

import json
import pprint


class EPManager(object):
    '''
    classdocs
    '''
    
    def __init__(self, sfc_db_, logger_):
        '''
        Constructor
        '''
        self.__ep_collection = sfc_db_.end_point
        self.__logger = logger_
        self.target = "end point"

    def parse_args(self, additional_options_enabled, additional_options_length, args):
        self.__logger.debug("args %s" % args)
        options = []
        if additional_options_enabled:
            if (len(args) != 1) and (len(args) % additional_options_length == 1):
                print 
                for i in range (0, len(args) / additional_options_length):
                    option = []
                    for j in range (0, additional_options_length):
                        option.append(args[i * additional_options_length + j + 1])
                        self.__logger.debug(option)
                    self.__logger.debug(option)
                    options.append(option)

        self.__logger.debug(options) 
        return options
    



    def create_entry(self, json_data=None, name=None, vlan=0, dpid=None, port=None):
        self.__logger.info("Create a service function forwarder")
        entry = {}
        
        if json_data != None:
            entry = json_data
        else:
            if name == None:
                self.__logger.error("please input the name of the service function forwarder with -n or --name option")
                exit
            if dpid == None:
                self.__logger.error("please input the dpid of the service function forwarder(e.g., 00:00:e4:11:5b:12:89:7e with -d or --dpid option")
                exit
            if port == None:
                self.__logger.error("please input the type of the service function forwarder(e.g., general, DASAN with -t or --type option")
                exit
            
            entry ["name"] = name
            entry ["vlan"] = vlan
            entry ["attached_switch"] = {}
            entry ["attached_switch"]["dpid"] = dpid
            entry ["attached_switch"]["attached_port"] = port
        
        
        result = self.validate_entry(entry) 
        if result == -1:
            return 0
        
        cursor = self.__ep_collection.find({"name": entry ["name"]})
        count = cursor.count()
        
        if count > 0:
            self.__logger.error("already, the end point is exist")
            return -1
        
        with open('result.json', 'w') as fp:
            json.dump(entry, fp)
        
        self.__ep_collection.insert(entry)
        self.__logger.debug(entry)
        self.__logger.info("the end point is completed")
        
    
    def validate_entry(self, entry):
        self.__logger.info("validate service_function_forwarder_enty")
        
        if entry ["name"] != "":
            self.__logger.debug("EP name is OK")
        else: 
            self.__logger.error("EP name is empty")
            return -1
        
        if entry ["attached_switch"]["dpid"] != "":
            self.__logger.debug("EP dpid is OK")
        else: 
            self.__logger.error("EP dpid is emply")
            return -1
            
        if entry ["attached_switch"]["attached_port"] != "":
            self.__logger.debug("EP dpid is OK")
        else: 
            self.__logger.error("EP dpid dpid is emply")
            return -1
            
        return 0

    def list_entry(self):
        print "list entries of the service function forwarder"
        cursor = self.__ep_collection.find()
        list = cursor[:]

        print "%s %s %s %s %s" % ("id".ljust(25), "name".ljust(20), "vlan".ljust(10), "dpid".ljust(25), "attached_switch_port".ljust(10))

            
        for document in list:
            print "%s" % str(document["_id"]).ljust(25),
            print "%s" % document["name"].ljust(20),
            print "%s" % str(document["vlan"]).ljust(10),
            print "%s" % document["attached_switch"]["dpid"].ljust(25),
            print "%s" % document["attached_switch"]["attached_port"].ljust(10),
            print ""
            
        return list
        
    
    def update_entry(self, json_data=None, name=None, vlan=None, dpid=None, port=None):
        self.__logger.info("Update end point")
        
        entry = "" 
        
        if json_data:
            exist = self.__ep_collection.find({"name": json_data["name"]}).count()
            entry = json_data["name"]
        elif name:
            exist = self.__ep_collection.find({"name": name}).count()
            entry = name
        else:
            return -1 
        
        self.__logger.debug("sff exist %s" % exist)

        if exist:
            self.delete_entry(entry)
            self.create_entry(json_data=json_data, name=name, vlan=vlan, dpid=dpid, port=port)
            self.__logger.info("Update %s success" % self.target)
 
        else:
            self.__logger.error("update fail, there is no inputed sf entry")
 

    def delete_entry(self, name="all"):
        self.__logger.info("delete the %s entrie" % self.target)
 
        if name == "all":
            result = self.__ep_collection.remove()
        else:
            result = self.__ep_collection.remove({"name": name})
        
        self.__logger.info("%s %s entries are deleted" % (result['n'], self.target))
