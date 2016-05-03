'''
Created on Nov 30, 2015

@author: root
'''
"""
{'Endian': {'egress_interface': {'ip': '192.168.0.30',
                 'mac': '52:54:00:63:6f:85',
                 'name': 'eth2'},
            'ingress_interface': {'ip': '',
                                  'mac': '52:54:00:37:a6:2d',
                                  'name': 'eth1'},
            'name': 'Endian',
            'type': 'DPI'}            """

import pprint


class SFManager(object):
    '''
    classdocs
    '''


    def __init__(self, sfc_db_, logger_):
        '''
        Constructor
        '''
        self.__DBcollection = sfc_db_.service_functions
        self.__logger = logger_
    
    def parse_args(self, additional_options_enabled, additional_options_length, args):
        self.__logger.debug("args %s" % args)
        options = []
        if additional_options_enabled:
            if (len(args) != 1) and (len(args) % additional_options_length == 1):
                for i in range (0, len(args) / additional_options_length):
                    option = []
                    for j in range (0, additional_options_length):
                        option.append(args[i * additional_options_length + j + 1])
                        self.__logger.debug(option)
                    self.__logger.debug(option)
                    options.append(option)

        self.__logger.debug(options) 
        return options
    
    def create_entry(self, json_data=None, name=None, type=None, ip=None, options=None):
        self.__logger.info("Create a service function [ex: firewall, NAT, DPI]")
        service_function_enty = {}
        
        if json_data != None:
            service_function_enty = json_data
        
        else:
            if name == None:
                self.__logger.error("please input the name of the service function (e.g., Cisco ASA Firewall) with -n or --name option")
                exit
            if type == None:
                self.__logger.error("please input the type of the service function (e.g., Firewall (FW), Deep Packet Inspection (DPI)) with -t or --type option ")
                exit
            if ip == None:
                self.__logger.error("please input the ip of the service function (e.g., Firewall (FW), Deep Packet Inspection (DPI)) with -t or --type option ")
                exit
            if options == None:    
                self.__logger.error("please input the type of the interface info -i or --interface option ")
                exit
            
            service_function_enty ["name"] = name
            service_function_enty ["ip"] = ip
            service_function_enty ["type"] = type
             
            interfaces = {}
            service_function_enty ["interfaces"] = interfaces
            for option in options:
                interface = {}
                interface["name"] = option[0]
                interface["ip"] = option[1]
                interface["mac"] = option[2]
                interface["type"] = option[3]
                interfaces[interface["name"]] = interface
                 
        result = self.validate_entry(service_function_enty) 
        if result == -1:
            return -1
        
        cursor = self.__DBcollection.find({"name": service_function_enty ["name"]})
        count = cursor.count()
        
        if count > 0:
            self.__logger.error("already, the service function is exist")
            return -1
        
        self.__DBcollection.insert(service_function_enty)
        self.__logger.debug(service_function_enty)
        self.__logger.info("The service function insertion is completed")
        
    
    def validate_entry(self, service_function_entry):
        print service_function_entry
        
        if service_function_entry ["name"] != "":
            self.__logger.debug("The SF name is OK (%s)" % service_function_entry ["name"])
        else: 
            self.__logger.error("The SF name is empty")
            return -1
        
        if (service_function_entry ["type"] != ""):
            self.__logger.debug("The SF Type is OK(%s)" % service_function_entry ["type"])
        else: 
            self.__logger.error("The SF Type is emply")
            return -1
            

        if service_function_entry["interfaces"] != None:    
            for interface in service_function_entry["interfaces"].values():
                if interface["name"] != "":
                    self.__logger.debug("The interfaces name is OK (%s)" % interface["name"])
                else:
                    self.__logger.error("The interfaces name is emply")
                    return -1
                
                if interface["mac"] != None:
                    self.__logger.debug("The interfaces MAC is OK (%s)" % interface["mac"])
                else: 
                    self.__logger.debug("The interfaces MAC is emply")
                    return -1
                
        return 0

    def list_entry(self):
        print "list entries of the service function"
        cursor = self.__DBcollection.find()
        list = cursor[:]
        
        print "%s %s %s %s %s" % ("id".ljust(25), "name".ljust(15), "ip".ljust(20), "type".ljust(10), "interfaces".ljust(30))
        
        for document in list:
            print "%s" % str(document["_id"]).ljust(25),
            print "%s" % document["name"].ljust(15),
            print "%s" % document["ip"].ljust(20),
            print "%s" % document["type"].ljust(10),
            print "%s" % str(document["interfaces"]).ljust(30),
            print ""
            
        return list
        
    
    def update_entry(self, json_data=None, name=None, type=None, ip=None, interfaces=None):
        self.__logger.info("starting update_entry")
        # sfc_db.service_functions.find({"name": name})
        sf_name = "" 
        
        if json_data:
            exist = self.__DBcollection.find({"name": json_data["name"]}).count()
            sf_name = json_data["name"]
        
        elif name:
            exist = self.__DBcollection.find({"name": name}).count()
            sf_name = name
        
        else:
            return -1 
        
        print exist
        if exist:
            self.delete_entry(sf_name)
            self.create_entry(json_data=json_data, name=sf_name, type=type, ip=ip, interfaces=interfaces)
            self.__logger.info("The service function update is success")
        else:
            self.__logger.error("update fail, there is no inputed sf entry")
          

    def delete_entry(self, name="all"):
        self.__logger.info("delete the service function entrie")
        if name == "all":
            result = self.__DBcollection.remove()
        else:
            result = self.__DBcollection.remove({"name": name})
        
        self.__logger.info("%s service entries are deleted" % result['n'])
