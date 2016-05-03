'''
Created on Nov 30, 2015

@author: root
'''

import json


class tenantManager(object):
    '''
    classdocs
    '''

    def __init__(self, sfc_db_, logger_):
        '''
        Constructor
        '''
        self.__tenant_collection = sfc_db_.tenant
        self.__logger = logger_
    
    def parse_args(self, opts_enabled, args):
        self.__logger.debug("args %s" % args)
        options = {}
        if opts_enabled:
            if (len(args) != 1) and (len(args) % 2 == 1):
                for i in range (0, len(args) / 2):
                    options[args[i * 3 + 1]] = args[i * 3 + 2]
                    
        self.__logger.debug("options %s" % options)
        return options

    def create_entry(self, json_data=None, name=None, priority=None, attributes=None):
        self.__logger.info("create tenant [ex: firewall, NAT, DPI]")
        tenant_entry = {}
        
        if json_data != None:
            tenant_entry = json_data
            
        else:
            if name == None:
                self.__logger.error("please input the name of the tenant  [ex: custumer A, custumer B]")
                return -1
                 
            if priority == None:
                self.__logger.error("please input the data path priority of tenant (0 ~ 65535): ")
                return -1
                
            tenant_entry ["name"] = name
            tenant_entry ["priority"] = priority
            tenant_entry ["attributes"] = attributes
        
         
        result = self.validate_entry(tenant_entry) 
        if result == -1:
            return 0
        
        cursor = self.__tenant_collection.find({"name": tenant_entry ["name"]})
        count = cursor.count()
        
        if count > 0:
            self.__logger.error("already, the tenant is exist")
            return -1
        
        with open('result.json', 'w') as fp:
            json.dump(tenant_entry, fp)
        
        self.__tenant_collection.insert(tenant_entry)
        self.__logger.debug(tenant_entry)
        self.__logger.info("Tanant is completed")
    
    def validate_entry(self, entry):
        self.__logger.debug(entry)
        
        if entry ["name"] != "":
            self.__logger.debug("name is OK")
        else: 
            self.__logger.error("error")
            return -1
        
        if entry ["priority"] != "":
            self.__logger.debug("priority is OK")
        else: 
            self.__logger.error("error")
            return -1

        if entry["attributes"] != None:    
            for value in entry["attributes"].values():
                self.__logger.debug("attributes %s" % value)

        return 0

    def list_entry(self):
        print "list entries of the service function forwarder"
        cursor = self.__tenant_collection.find()
        list = cursor[:]
        
        print "%s %s %s %s" % ("id".ljust(25), "name".ljust(15), "priority".ljust(20), "attributes".ljust(30))
        
        for document in list:
            print "%s" % str(document["_id"]).ljust(25),
            print "%s" % document["name"].ljust(15),
            print "%s" % document["priority"].ljust(20),
            print "%s" % str(document["attributes"]).ljust(30),
            print ""
            
        return list
        
    
    def update_entry(self, json_data=None, name=None, priority=None, attributes=None):
        self.__logger.info("update tenant")

        entry_name = "" 
        if json_data:
            exist = self.__tenant_collection.find({"name": json_data["name"]}).count()
            entry_name = json_data["name"]
        elif name:
            exist = self.__tenant_collection.find({"name": name}).count()
            entry_name = name
        else:
            return -1 
        
        self.__logger.debug("%s exist %s" % (entry_name, exist))
        
        if exist:
            self.delete_entry(entry_name)
            self.create_entry(json_data=json_data, name=entry_name, priority=priority, attributes=attributes)
            self.__logger.info("update success")
 
        else:
            self.__logger.info("update fail, there is no inputed tanant entry")
          

    def delete_entry(self, name="all"):
        self.__logger.info("delete the tenant entries")
        
        if name == "all":
            result = self.__tenant_collection.remove()
        else:
            result = self.__tenant_collection.remove({"name": name})
        
        self.__logger.info("%s entries are deleted" % result['n'])           
