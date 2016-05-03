'''
Created on Nov 30, 2015

@author: root
'''
"""
 '00:00:00:0c:29:57:3d:a4': {'connected_sf': {'Endian': {'egress_port': 14,
                                             'ingress_port': 13},
                                  'vDPI': {'egress_port': 5,
                                           'ingress_port': 4},
                                  'vFW': {'egress_port': 2,
                                          'ingress_port': 1}},
                                 'dpid': '00:00:00:0c:29:57:3d:a4',
                                 'name': 'OpenvSwitch A',
                                 'type': 'general'} """

import json
import pprint



class SFFManager(object):
    '''
    classdocs
    '''


    def __init__(self, sfc_db_, logger_):
        '''
        Constructor
        '''
        self.__sff_collection = sfc_db_.service_function_forwarder
        self.__logger = logger_

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
    


    def create_entry(self, json_data=None, name=None, dpid=None, type=None, options=None):
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
            if type == None:
                self.__logger.error("please input the type of the service function forwarder(e.g., general, DASAN with -t or --type option")
                exit
            
            entry ["name"] = name
            entry ["dpid"] = dpid
            entry ["type"] = type
            
            if options != None:
                connected_sfs = {}
                entry ["connected_sf"] = connected_sfs
                for option in options:
                    connected_sf = {}
                    connected_sf["name"] = option[0]
                    connected_sf["ingress_port"] = option[1]
                    connected_sf["egress_port"] = option[2]
                    connected_sfs[connected_sf["name"]] = connected_sf
        
        result = self.validate_entry(entry) 
        if result == -1:
            return 0
        
        cursor = self.__sff_collection.find({"name": entry ["name"]})
        count = cursor.count()
        
        if count > 0:
            self.__logger.error("already, the service function is exist")
            return -1
        
        with open('result.json', 'w') as fp:
            json.dump(entry, fp)
        
        self.__sff_collection.insert(entry)
        self.__logger.debug(entry)
        self.__logger.info("The service function creation is completed")
        
    
    def validate_entry(self, entry):
        self.__logger.info("validate entry")
        
        if entry ["name"] != "":
            self.__logger.debug("SFF name is OK")
        else: 
            self.__logger.error("SFF name is empty")
            return -1
        
        if (entry ["type"] == "general") or (entry ["type"] == "DASAN"):
            self.__logger.debug("SFF type is OK")
        else: 
            self.__logger.error("SFF type is wrong (%s)" % entry ["type"])
            return -1
            
        if entry ["dpid"] != "":
            self.__logger.debug("SFF dpid is OK(%s)" % entry ["dpid"])
        else: 
            self.__logger.error("SFF dpid is wrong (%s)" % entry ["dpid"])
            return -1
            
        if entry["connected_sf"] != None:    
            for sf in entry["connected_sf"].values():
                if sf["name"] != "":
                    self.__logger.debug("connected_sf's name is OK (%s)" % sf["name"])
                else:
                    self.__logger.error("connected_sf's name is wrong (%s)" % sf["name"])
                    return -1
                
                if sf["ingress_port"]:
                    self.__logger.debug("connected_sf's ingress_port is OK (%s)" % sf["ingress_port"])
                else: 
                    self.__logger.error("connected_sf's ingress_port is wrong (%s)" % sf["ingress_port"])
                    return -1
                
                if sf["egress_port"]:
                    self.__logger.debug("connected_sf's egress_port is OK (%s)" % sf["egress_port"])
                else: 
                    self.__logger.debug("connected_sf's egress_port is wrong (%s)" % sf["egress_port"])
                    return -1
        return 0

    def list_entry(self):
        print "list entries of the service function forwarder"
        cursor = self.__sff_collection.find()
        list = cursor[:]
        
        print "%s %s %s %s %s" % ("id".ljust(25), "name".ljust(15), "dpid".ljust(25), "type".ljust(10), "connected_sf".ljust(30))
        
        for document in list:
            print "%s" % str(document["_id"]).ljust(25),
            print "%s" % document["name"].ljust(15),
            print "%s" % document["dpid"].ljust(25),
            print "%s" % document["type"].ljust(10),
            print "%s" % str(document["connected_sf"]).ljust(30),
            print ""
            
        return list
        
    
    def update_entry(self, json_data=None, name=None, type=None, dpid=None, options=None):
        self.__logger.info("Update sff")
        
        sff_name = "" 
        
        if json_data:
            exist = self.__sff_collection.find({"name": json_data["name"]}).count()
            sff_name = json_data["name"]
        elif name:
            exist = self.__sff_collection.find({"name": name}).count()
            sff_name = name
        else:
            return -1 
        
        self.__logger.debug("sff exist %s" % exist)

        if exist:
            self.delete_entry(sff_name)
            self.create_entry(json_data=json_data, name=sff_name, dpid=dpid, type=type, options=options)
            self.__logger.info("Update sff success")
 
        else:
            self.__logger.error("update fail, there is no inputed sf entry")
 

    def delete_entry(self, name="all"):
        self.__logger.info("delete the service function entrie")
 
        if name == "all":
            result = self.__sff_collection.remove()
        else:
            result = self.__sff_collection.remove({"name": name})
        
        self.__logger.info("%s service entries are deleted" % result['n'])
