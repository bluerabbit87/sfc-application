'''
Created on Nov 30, 2015

@author: root
'''

"""'ns_dict_1': {'vnffg_list': 'vnffg_list_1',
   'egress_endpoint': 'egress_endpoint',
   'ingress_endpoint': 'ingress_endpoint',
   'name': 'ns_dict_1',"""
            
import json
import pprint


class NSManager(object):
    '''
    classdocs
    '''

    def __init__(self, sfc_db_, logger_):
        '''
        Constructor
        '''
        self.__DBcollection = sfc_db_.network_service
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

    def create_entry(self, json_data=None, name=None, ingress_endpoint=None, egress_endpoint=None , vnffg=None, tenant=None):
        self.__logger.info("create network service entry [ex: firewall, NAT, DPI]")
                
       
        entry = {}
        if json_data != None:
            entry = json_data
            
        else:
            if name == None:
                self.__logger.error("please input the name of the service function forwarder with -n or --name option")
                return -1
                
            if ingress_endpoint == None:
                self.__logger.error("please input the name of the ingress_endpoint  [ex: custumer A, custumer B] : ")
                return -1 
            
            if egress_endpoint == None:
                self.__logger.error("please input the name of the egress_endpoint  [ex: custumer A, custumer B] : ")
                return -1
                
            if tenant == None:
                entry ["tenant"] = "default"
                # self.__logger.error("please input the name of the tenant  [ex: custumer A, custumer B] : ")
                # return -1 
            else:
                entry ["tenant"] = tenant
    
            
            entry ["name"] = name
            entry ["ingress_endpoint"] = ingress_endpoint
            entry ["egress_endpoint"] = egress_endpoint
            entry ["vnffg"] = vnffg
            
            #
        
         
        result = self.validate_entry(entry) 
        if result == -1:
            return 0
        
        cursor = self.__DBcollection.find({"name": entry ["name"]})
        count = cursor.count()
        
        if count > 0:
            self.__logger.error("already, the service function is exist")
            return -1
        
        with open('result.json', 'w') as fp:
            json.dump(entry, fp)
        
        self.__DBcollection.insert(entry)
        self.__logger.debug(entry)
        self.__logger.info("The network service insertion is completed")
            
    
    def validate_entry(self, entry):
        self.__logger.info("validate_entry")
        
        print entry
        if entry ["name"] != "":
            self.__logger.debug("name is ok")
        else: 
            self.__logger.error("name is empty")
            return -1
        
        if entry ["ingress_endpoint"] != "":
            self.__logger.debug("ingress_endpoint is OK")
        else: 
            self.__logger.error("ingress_endpoint is empty")
            return -1
        
        if entry ["egress_endpoint"] != "":
            self.__logger.debug("egress_endpoint is OK")
        else: 
            self.__logger.debug("egress_endpoint is empty")
            return -1
        
#         if entry ["vnffg"] != "":
#             self.__logger.debug("vnffg is OK")
#         else: 
#             self.__logger.warn("vnffg is empty")
            
        return 0

    def list_entry(self):
        print "list entries of the service function forwarder"
        cursor = self.__DBcollection.find()
        list = cursor[:]
        
        print "%s %s %s %s %s %s" % ("id".ljust(25), "name".ljust(15), "ingress_endpoint".ljust(20), "egress_endpoint".ljust(20), "tenant".ljust(15), "VNF Forwarding Graph".ljust(30))
        
        for document in list:
            print "%s" % str(document["_id"]).ljust(25),
            print "%s" % document["name"].ljust(15),
            print "%s" % document["ingress_endpoint"].ljust(20),
            print "%s" % document["egress_endpoint"].ljust(20),
            print "%s" % str(document["tenant"]).ljust(15),
            print "%s" % str(document["vnffg"]).ljust(30),
            
            print ""
            
        return list
        
    
    def update_entry(self, json_data=None, name=None, ingress_endpoint=None, egress_endpoint=None , vnffg=None, tenant=None):
        self.__logger.info("update network service")
        
        entry_name = "" 
        if json_data:
            exist = self.__DBcollection.find({"name": json_data["name"]}).count()
            entry_name = json_data["name"]
        elif name:
            exist = self.__DBcollection.find({"name": name}).count()
            entry_name = name
        else:
            return -1 
        
        self.__logger.info("%s exist %s" % (entry_name, exist))
        
        if exist:
            self.delete_entry(entry_name)
            self.create_entry(json_data=json_data, name=entry_name, ingress_endpoint=ingress_endpoint, egress_endpoint=egress_endpoint , vnffg=vnffg, tenant=tenant)
            self.__logger.info("update success")
        
        else:
            self.__logger.info("update fail, there is no inputed sf entry")
          

    def delete_entry(self, name="all"):
        self.__logger.info("delete the network serivce entrie")
        if name == "all":
            result = self.__DBcollection.remove()
        else:
            result = self.__DBcollection.remove({"name": name})
        
        self.__logger.info("%s entries are deleted" % result['n'])
