import pprint
import sys

from floodlight.floodlight_agent import OpenFlowHandler


# 
# sys.path.append('/root/workspace/PSDN Projects/')
# sys.path.append('/home/sdn/PSDN Projects/')
# sys.path.append('/home/sdn/sfc/sfc/')
# service_function_1 = {}
# service_function_1["name"]                      = "vFW"
# service_function_1["type"]                      = "Firewall"
#  
# service_function_1["ingress_interface"]         = {}
# service_function_1["ingress_interface"]["name"] = "eth1"
# service_function_1["ingress_interface"]["ip"]   = "10.0.10.1"
# service_function_1["ingress_interface"]["mac"]  = "52:54:00:48:4e:8a"
#  
# service_function_1["egress_interface"]          = {}
# service_function_1["egress_interface"]["name"]  = "eth2"
# service_function_1["egress_interface"]["ip"]    = "192.168.10.1"
# service_function_1["egress_interface"]["mac"]   = "52:54:00:f8:4a:02"
#                                              
# service_function_2 = {}
# service_function_2["name"]                      = "vDPI"
# service_function_2["type"]                      = "DPI"
#  
# service_function_2["ingress_interface"]         = {}
# service_function_2["ingress_interface"]["name"] = "eth1"
# service_function_2["ingress_interface"]["ip"]   = "10.0.10.2"
# service_function_2["ingress_interface"]["mac"]  = "52:54:00:6d:96:e9"
#  
#  
# service_function_2["egress_interface"]          = {}
# service_function_2["egress_interface"]["name"]  = "eth2"
# service_function_2["egress_interface"]["ip"]    = "192.168.10.2"
# service_function_2["egress_interface"]["mac"]   = "52:54:00:60:f7:82"
#  
# service_function_3 = {}
# service_function_3["name"]                      = "Endian"
# service_function_3["type"]                      = "UTM"
#  
# service_function_3["ingress_interface"]         = {}
# service_function_3["ingress_interface"]["name"] = "eth1"
# service_function_3["ingress_interface"]["ip"]   = ""
# service_function_3["ingress_interface"]["mac"]  = "52:54:00:37:a6:2d"
#  
#  
# service_function_3["egress_interface"]          = {}
# service_function_3["egress_interface"]["name"]  = "eth2"
# service_function_3["egress_interface"]["ip"]    = "192.168.0.30"
# service_function_3["egress_interface"]["mac"]   = "52:54:00:63:6f:85"
#  
# service_function_4 = {}
# service_function_4["name"]                      = "Endian A"
# service_function_4["type"]                      = "UTM"
#  
# #sdn port 9, vnet 5
# service_function_4["ingress_interface"]         = {}
# service_function_4["ingress_interface"]["name"] = "eth1"
# service_function_4["ingress_interface"]["ip"]   = ""
# service_function_4["ingress_interface"]["mac"]  = "52:54:00:E9:4F:B9"
#  
# #sdn port 10, vnet 6
# service_function_4["egress_interface"]          = {}
# service_function_4["egress_interface"]["name"]  = "eth2"
# service_function_4["egress_interface"]["ip"]    = ""
# service_function_4["egress_interface"]["mac"]   = "52:54:00:B0:29:68"
#  
# service_function_5 = {}
# service_function_5["name"]                      = "Endian B"
# service_function_5["type"]                      = "UTM"
#  
# #sdn port 7, vnet 1
# service_function_5["ingress_interface"]         = {}
# service_function_5["ingress_interface"]["name"] = "eth1"
# service_function_5["ingress_interface"]["ip"]   = ""
# service_function_5["ingress_interface"]["mac"]  = "52:54:00:7C:A8:50"
#  
# #sdn port 8, vnet 2
# service_function_5["egress_interface"]          = {}
# service_function_5["egress_interface"]["name"]  = "eth2"
# service_function_5["egress_interface"]["ip"]    = ""
# service_function_5["egress_interface"]["mac"]   = "52:54:00:13:1E:D7"
#  
# #SF interfaces info could be collected by virsh (libvirt tool)
# #virsh edit "VM NAME"
#  
# SF_collection = {}
# SF_collection["vFW"]            = service_function_1
# SF_collection["vDPI"]           = service_function_2
# SF_collection["Endian"]         = service_function_3
# SF_collection["Endian A"]       = service_function_4
# SF_collection["Endian B"]       = service_function_5
#   
# pprint.pprint(SF_collection)
#   
# service_function_forwarder_1 = {}
# service_function_forwarder_1 ["name"]           = "OpenvSwitch A"
# service_function_forwarder_1 ["dpid"]           = "00:00:00:0c:29:57:3d:a4"
# service_function_forwarder_1 ["type"]           = "general"
# service_function_forwarder_1 ["connected_sf"]   = {}
#  
# service_function_forwarder_1 ["connected_sf"]["vFW"] = {}
# service_function_forwarder_1 ["connected_sf"]["vFW"]["ingress_port"] = 1
# service_function_forwarder_1 ["connected_sf"]["vFW"]["egress_port"]  = 2
#  
# service_function_forwarder_1 ["connected_sf"]["vDPI"]   = {}
# service_function_forwarder_1 ["connected_sf"]["vDPI"]["ingress_port"]   = 4
# service_function_forwarder_1 ["connected_sf"]["vDPI"]["egress_port"]    = 5
#  
# service_function_forwarder_1 ["connected_sf"]["Endian"]   = {}
# service_function_forwarder_1 ["connected_sf"]["Endian"]["ingress_port"]   = 13
# service_function_forwarder_1 ["connected_sf"]["Endian"]["egress_port"]    = 14
#  
# service_function_forwarder_2 = {}
# service_function_forwarder_2 ["name"]           = "OpenvSwitch B"
# service_function_forwarder_2 ["dpid"]           = "00:00:e4:11:5b:12:89:7e"
# service_function_forwarder_2 ["type"]           = "general"
# service_function_forwarder_2 ["connected_sf"]   = {}
#  
# service_function_forwarder_2 ["connected_sf"]["Endian A"] = {}
# service_function_forwarder_2 ["connected_sf"]["Endian A"]["ingress_port"] = 9
# service_function_forwarder_2 ["connected_sf"]["Endian A"]["egress_port"]  = 10
#  
# service_function_forwarder_2 ["connected_sf"]["Endian B"]   = {}
# service_function_forwarder_2 ["connected_sf"]["Endian B"]["ingress_port"]   = 7
# service_function_forwarder_2 ["connected_sf"]["Endian B"]["egress_port"]    = 8
# #Connection info between SFF and SF could be collected by sudo ovsdb-client dump
#  
# service_function_forwarder_3 = {}
# service_function_forwarder_3 ["name"]           = "DASAN A"
# service_function_forwarder_3 ["dpid"]           = "00:00:00:00:00:00:00:01"
# service_function_forwarder_3 ["type"]           = "DASAN"
# service_function_forwarder_3 ["connected_sf"]   = {}
#  
#  
# #Connection info between SFF and SF could be collected by sudo ovsdb-client dump
#  
#  
# self.__SFF_collection = {}
# self.__SFF_collection["00:00:00:0c:29:57:3d:a4"] = service_function_forwarder_1
# self.__SFF_collection["00:00:e4:11:5b:12:89:7e"] = service_function_forwarder_2
# self.__SFF_collection["00:00:00:00:00:00:00:01"] = service_function_forwarder_3
#   
# pprint.pprint(self.__SFF_collection)
#   
# end_point_1 = {}
# end_point_1["name"]= "ingress_endpoint"
# end_point_1["vlan"]= 0
# end_point_1["attached_switch"] = {}
# end_point_1["attached_switch"]["dpid"]= "00:00:00:0c:29:57:3d:a4"
# end_point_1["attached_switch"]["attached_port"]= 9
#  
# end_point_2 = {}
# end_point_2["name"]= "egress_endpoint"
# end_point_2["vlan"]= 0
# end_point_2["attached_switch"] = {}
# end_point_2["attached_switch"]["dpid"]= "00:00:00:0c:29:57:3d:a4"
# end_point_2["attached_switch"]["attached_port"]= 3
#  
# end_point_3 = {}
# end_point_3["name"]= "ingress_endpoint B"
# end_point_3["vlan"]= 0
# end_point_3["attached_switch"] = {}
# end_point_3["attached_switch"]["dpid"]= "00:00:e4:11:5b:12:89:7e"
# end_point_3["attached_switch"]["attached_port"]= 1
#  
# end_point_4 = {}
# end_point_4["name"]= "egress_endpoint B"
# end_point_4["vlan"]= 0
# end_point_4["attached_switch"] = {}
# end_point_4["attached_switch"]["dpid"]= "00:00:e4:11:5b:12:89:7e"
# end_point_4["attached_switch"]["attached_port"]= 2
#  
# end_point_5 = {}
# end_point_5["name"]= "DASAN endpoint"
# end_point_5["vlan"]= 0
# end_point_5["attached_switch"] = {}
# end_point_5["attached_switch"]["dpid"]= "00:00:00:00:00:00:00:01"
# end_point_5["attached_switch"]["attached_port"]= 1
#  
#  
# self.__EP_collection = {}
# self.__EP_collection["ingress_endpoint"]    = end_point_1
# self.__EP_collection["egress_endpoint"]     = end_point_2
# self.__EP_collection["ingress_endpoint B"]  = end_point_3
# self.__EP_collection["egress_endpoint B"]   = end_point_4
# self.__EP_collection["DASAN endpoint"]      = end_point_5
#   
# pprint.pprint(self.__EP_collection)
#   
# VNFFG_1 = {"name":"VNFFG_1","sf_list":["vDPI"]}
# VNFFG_2 = {"name":"VNFFG_2","sf_list":["vDPI","vFW"]} 
# VNFFG_3 = {"name":"VNFFG_3","sf_list":["vFW","vDPI"]}  
# VNFFG_4 = {"name":"VNFFG_4","sf_list":["Endian"]}  
# VNFFG_5 = {"name":"VNFFG_5","sf_list":["Endian A"]}  
# VNFFG_6 = {"name":"VNFFG_6","sf_list":["Endian B"]}  
# VNFFG_7 = {"name":"VNFFG_7","sf_list":["Endian A", "Endian B"]}  
#  
#  
# self.__VNFFG_collection = {}
# self.__VNFFG_collection["VNFFG_1"] = VNFFG_1
# self.__VNFFG_collection["VNFFG_2"] = VNFFG_2
# self.__VNFFG_collection["VNFFG_3"] = VNFFG_3
# self.__VNFFG_collection["VNFFG_4"] = VNFFG_4
# self.__VNFFG_collection["VNFFG_5"] = VNFFG_5
# self.__VNFFG_collection["VNFFG_6"] = VNFFG_6
# self.__VNFFG_collection["VNFFG_7"] = VNFFG_7
#   
# pprint.pprint(self.__VNFFG_collection)
#   
# tenant_1 = {}
# tenant_1["name"]  = "default"
# tenant_1["attributes"] = {}
# tenant_1["priority"] = 1000
#  
# tenant_2 = {}
# tenant_2["name"]  = "arp_traffic"
# tenant_2["attributes"] = {}
# tenant_2["attributes"]["eth_type"]="0x0806"
# tenant_2["priority"] = 1000
#  
# tenant_3 = {}
# tenant_3["name"]  = "udp_traffic"
# tenant_3["attributes"] = {}
# tenant_3["attributes"]["eth_type"]="0x0800"
# tenant_3["attributes"]["ip_proto"]="17"
# tenant_3["priority"] = 1000
#  
# tenant_4 = {}
# tenant_4["name"]  = "tcp_traffic"
# tenant_4["attributes"] = {}
# tenant_4["attributes"]["eth_type"]="0x0800"
# tenant_4["attributes"]["ip_proto"]="6"
# tenant_4["priority"] = 1000
#  
# tenant_5 = {}
# tenant_5["name"]  = "vlan_traffic"
# tenant_5["attributes"] = {}
# tenant_5["attributes"]["eth_type"]="0x0800"
# tenant_5["attributes"]["ip_proto"]="6"
# tenant_5["priority"] = 1000
#  
# tenant_6 = {}
# tenant_6["name"]  = "src_ip_traffic"
# tenant_6["attributes"] = {}
# tenant_6["attributes"]["eth_type"]="0x0800"
# tenant_6["attributes"]["ip_proto"]="6"
# tenant_6["attributes"]["ipv4_src"]="10.0.0.10"
# tenant_6["priority"] = 1000
#  
#  
# self.__tenant_collection = {}
# self.__tenant_collection["default"]            = tenant_1
# self.__tenant_collection["arp_traffic"]        = tenant_2
# self.__tenant_collection["udp_traffic"]        = tenant_3
# self.__tenant_collection["tcp_traffic"]        = tenant_4
# self.__tenant_collection["src_ip_traffic"]     = tenant_5
# self.__tenant_collection["vlan_traffic"]       = tenant_6
#   
# pprint.pprint(self.__tenant_collection)
#  
# ns_dict_0 = {}
# ns_dict_0["name"]= "ns_dict_0"
# ns_dict_0["ingress_endpoint"] = "ingress_endpoint"
# ns_dict_0["egress_endpoint"] = "egress_endpoint"
# ns_dict_0["VNFFG"] = None
# ns_dict_0["tenant"]   = "default"
# 
# ns_dict_1 = {}
# ns_dict_1["name"]= "ns_dict_1"
# ns_dict_1["ingress_endpoint"] = "ingress_endpoint"
# ns_dict_1["egress_endpoint"] = "egress_endpoint"
# ns_dict_1["VNFFG"] = "VNFFG_1"
# ns_dict_1["tenant"]   = "default"
# 
# ns_dict_2 = {}
# ns_dict_2["name"]="ns_dict_2"
# ns_dict_2["ingress_endpoint"] = "ingress_endpoint"
# ns_dict_2["egress_endpoint"] = "egress_endpoint"
# ns_dict_2["VNFFG"] = "VNFFG_2"
# ns_dict_2["tenant"]   = "default"
# 
# ns_dict_3 = {}
# ns_dict_3["name"]="ns_dict_3"
# ns_dict_3["ingress_endpoint"] = "ingress_endpoint"
# ns_dict_3["egress_endpoint"] = "egress_endpoint"
# ns_dict_3["VNFFG"] = "VNFFG_3"
# ns_dict_3["tenant"]   = "default"
# 
# ns_dict_4 = {}
# ns_dict_4["name"]="ns_dict_4"
# ns_dict_4["ingress_endpoint"] = "ingress_endpoint"
# ns_dict_4["egress_endpoint"] = "egress_endpoint"
# ns_dict_4["VNFFG"] = "VNFFG_3"
# ns_dict_4["tenant"]   = "udp_traffic"
# 
# ns_dict_5 = {}
# ns_dict_5["name"]="ns_dict_5"
# ns_dict_5["ingress_endpoint"] = "ingress_endpoint"
# ns_dict_5["egress_endpoint"] = "egress_endpoint"
# ns_dict_5["VNFFG"] = "VNFFG_3"
# ns_dict_5["tenant"]   = "vlan_traffic"
# 
# ns_dict_6 = {}
# ns_dict_6["name"]="ns_dict_6"
# ns_dict_6["ingress_endpoint"] = "ingress_endpoint"
# ns_dict_6["egress_endpoint"] = "egress_endpoint"
# ns_dict_6["VNFFG"] = "VNFFG_3"
# ns_dict_6["tenant"]   = "src_ip_traffic"
# 
# ns_dict_7 = {}
# ns_dict_7["name"]= "ns_dict_7"
# ns_dict_7["ingress_endpoint"] = "ingress_endpoint"
# ns_dict_7["egress_endpoint"] = "egress_endpoint"
# ns_dict_7["VNFFG"] = "VNFFG_4"
# ns_dict_7["tenant"]   = "default"
# 
# ns_dict_8 = {}
# ns_dict_8["name"]= "ns_dict_8"
# ns_dict_8["ingress_endpoint"] = "ingress_endpoint B"
# ns_dict_8["egress_endpoint"] = "egress_endpoint B"
# ns_dict_8["VNFFG"] = ""
# ns_dict_8["tenant"]   = "default"
# 
# ns_dict_9 = {}
# ns_dict_9["name"]= "ns_dict_9"
# ns_dict_9["ingress_endpoint"] = "ingress_endpoint B"
# ns_dict_9["egress_endpoint"] = "egress_endpoint B"
# ns_dict_9["VNFFG"] = "VNFFG_5"
# ns_dict_9["tenant"]   = "default"
# 
# ns_dict_10 = {}
# ns_dict_10["name"]= "ns_dict_10"
# ns_dict_10["ingress_endpoint"] = "ingress_endpoint B"
# ns_dict_10["egress_endpoint"] = "egress_endpoint B"
# ns_dict_10["VNFFG"] = "VNFFG_6"
# ns_dict_10["tenant"]   = "default"
# 
# ns_dict_11 = {}
# ns_dict_11["name"]= "ns_dict_11"
# ns_dict_11["ingress_endpoint"] = "ingress_endpoint B"
# ns_dict_11["egress_endpoint"] = "egress_endpoint B"
# ns_dict_11["VNFFG"] = "VNFFG_7"
# ns_dict_11["tenant"]   = "default"
# 
# ns_dict_12 = {}
# ns_dict_12["name"]= "ns_dict_12"
# ns_dict_12["ingress_endpoint"] = "DASAN endpoint"
# ns_dict_12["egress_endpoint"] = "egress_endpoint B"
# ns_dict_12["VNFFG"] = ""
# ns_dict_12["tenant"]   = "default"
# 
# ns_dict_13 = {}
# ns_dict_13["name"]= "ns_dict_12"
# ns_dict_13["ingress_endpoint"] = "DASAN endpoint"
# ns_dict_13["egress_endpoint"] = "egress_endpoint B"
# ns_dict_13["VNFFG"] = "VNFFG_5"
# ns_dict_13["tenant"]   = "default"
# 
# ns_dict_14 = {}
# ns_dict_14["name"]= "ns_dict_12"
# ns_dict_14["ingress_endpoint"] = "DASAN endpoint"
# ns_dict_14["egress_endpoint"] = "egress_endpoint B"
# ns_dict_14["VNFFG"] = "VNFFG_6"
# ns_dict_14["tenant"]   = "default"
# 
# ns_dict_15 = {}
# ns_dict_15["name"]= "ns_dict_12"
# ns_dict_15["ingress_endpoint"] = "DASAN endpoint"
# ns_dict_15["egress_endpoint"] = "egress_endpoint B"
# ns_dict_15["VNFFG"] = "VNFFG_7"
# ns_dict_15["tenant"]   = "default"
# 
# 
# ns_collection = {}
# ns_collection["ns_dict_0"]  = ns_dict_0
# ns_collection["ns_dict_1"]  = ns_dict_1
# ns_collection["ns_dict_2"]  = ns_dict_2
# ns_collection["ns_dict_3"]  = ns_dict_3
# ns_collection["ns_dict_4"]  = ns_dict_4
# ns_collection["ns_dict_5"]  = ns_dict_5
# ns_collection["ns_dict_6"]  = ns_dict_6
# ns_collection["ns_dict_7"]  = ns_dict_7
# ns_collection["ns_dict_8"]  = ns_dict_8
# ns_collection["ns_dict_9"]  = ns_dict_9
# ns_collection["ns_dict_10"] = ns_dict_10
# ns_collection["ns_dict_11"] = ns_dict_11
# ns_collection["ns_dict_12"] = ns_dict_12
# ns_collection["ns_dict_13"] = ns_dict_13
# ns_collection["ns_dict_14"] = ns_dict_14
# ns_collection["ns_dict_15"] = ns_dict_15
# pprint.pprint(ns_collection)
class SFCManager ():
    """ Service Function Manager (SFC Manager) is responsible for parsing a service function path (SFP) and
    deploying correct openflow entries on OpenFlow Switches (OVS, Arista OpenFlow Switch, DASAN 1G ~ 10G) """
        
    OFhandler = None

    def __init__(self, OFHandler_=None, sfc_db=None, logger=None):
        # if no OpenFlowHandler have been provided, create default OpenFlow Handler
        
        if not OFHandler_:
            self.OFhandler = OpenFlowHandler("127.0.0.1", "8080")
        else:
            self.OFhandler = OFHandler_
            
        
        self.__SF_collection = sfc_db.service_function_forwarder
        self.__SFF_collection = sfc_db.service_function_forwarder
        self.__VNFFG_collection = sfc_db.VNF_forwarding_graph
        self.__tenant_collection = sfc_db.tenant
        self.__EP_collection = sfc_db.end_point
        self.__ns_collection = sfc_db.network_service
        self.__logger = logger
    
            
            
    def show_service_path(self, name):
        # Show Service Function Path entries
        Cursor = self.__ns_collection.find({"name": name})
        print Cursor.count()
        if Cursor.count() != 0:
            NS_entry = Cursor.next()
        else:
            return -1
        
         
        print "===================NS_entry==========================="
        print NS_entry
        print "NS_name\t: %s" % NS_entry["name"]
        
        print "tenant_info\t: %s" % NS_entry["tenant"]
        print "tenant_detail\t" 
        Cursor = self.__tenant_collection.find({"name": NS_entry["tenant"]})
        tenantEntry = ""
        print Cursor.count()
        
        if Cursor.count() != 0:
            tenantEntry = Cursor.next()
        else:
            return -1
        pprint.pprint(tenantEntry)
        
        print "ingress_endpoint_info"
        print NS_entry["ingress_endpoint"]
        Cursor = self.__EP_collection.find({"name": NS_entry["ingress_endpoint"]})
        ingress_endpoint_info = ""
        print Cursor.count()
        
        if Cursor.count() != 0:
            ingress_endpoint_info = Cursor.next()
        else:
            return -1
        pprint.pprint(ingress_endpoint_info)
        
        
        print "egress_endpoint_info"
        print NS_entry["egress_endpoint"]
        Cursor = self.__EP_collection.find({"name": NS_entry["egress_endpoint"]})
        egress_endpoint_info = ""
        print Cursor.count()
        
        if Cursor.count() != 0:
            egress_endpoint_info = Cursor.next()
        else:
            return -1
        pprint.pprint(egress_endpoint_info)
        
        
        print "VNFFG_name\t: %s" % (NS_entry["vnffg"])
        Cursor = self.__VNFFG_collection.find({"name": NS_entry["vnffg"]})
        VNFFG = ""
        print Cursor.count()
        
        if Cursor.count() != 0:
            VNFFG = Cursor.next()
            pprint.pprint(VNFFG)
        else:
            print "There is not a list of service function chaning"
            return -1
        
        
#         if NS_entry["vnffg"] != None:
#             print self.__VNFFG_collection[NS_entry["vnffg"]]
#         else:
#         
#         print "======================================================="
        
    def find_service_function_path(self, name):
        """rendros openflow entries using the provided service function path entry (NS_entry)
        :param NS_entry (e.g., {
                                    "name"             : "ns_dict_0",         (optional)
                                    "ingress_endpoint"  : "ingress_endpoint", (mandatory)
                                    "egress_endpoint"   : "egress_endpoint",  (mandatory)  
                                    "VNFFG"          : "VNFFG_1",        (optional)
                                    "tenant"            : "default"        (optional)
                                }
        :returns openflow entries that is rendered
        """
        
        # Check if the attributs of SFP entry are vaild
        Cursor = self.__ns_collection.find({"name": name})
        print Cursor.count()
        if Cursor.count() != 0:
            NS_entry = Cursor.next()
        else:
            return -1
        
        msg = self.validate_NS(name)
        if msg:
            print msg
            return -1
        
        # Load endpoints and sfc list informations 
        
        Cursor = self.__EP_collection.find({"name": NS_entry["ingress_endpoint"]})
        ingress_endpoint = Cursor.next()
        self.__logger.info("ingress_endpoint loading is completed(%s)" % NS_entry["ingress_endpoint"])
        
        Cursor = self.__EP_collection.find({"name": NS_entry["egress_endpoint"]})
        egress_endpoint = Cursor.next()
        self.__logger.info("egress_endpoint loading is completed(%s)" % NS_entry["egress_endpoint"])

        print "VNFFG_name\t: %s" % (NS_entry["vnffg"])
        Cursor = self.__VNFFG_collection.find({"name": NS_entry["vnffg"]})
        VNFFG = None
        print Cursor.count()
        
        if Cursor.count() != 0:
            VNFFG = Cursor.next()
            pprint.pprint(VNFFG)
        else:
            print "There is not a list of service function chaning"
            
        
        # tenant              =   self.__tenant_collection[NS_entry["tenant"]]
        
        # Find service path from ingress endpoint to egress enpoint including serfice function chaining path
        print "ingress %s" % ingress_endpoint
        print "egress %s" % egress_endpoint
        
        
        service_path = self.find_service_path(ingress_endpoint=ingress_endpoint,
                                              egress_endpoint=egress_endpoint,
                                              VNFFG=VNFFG)
        
        print "service path: %s" % (service_path)
        return service_path
    
#         if not service_path:
#             print "cannot find possible route for the service path"
#             return None
#         
#         rendered_path = self.rendor_floodlight_static_pusher_json(NS_entry["name"],
#                                                                   service_path,
#                                                                   tenant)
        
#         return rendered_path
    
    def validate_NS(self, name):
        """Check if the attributs of SFP entry are vaild
        
        If medetory attributes are empty then the method will return error message.
        If optional attributes are empty then the method will set default conf.
        If all is OK then it will return None.  
        
        """
        
        self.__logger.info("validate_NS")
        
        NS_entry = ''
        Cursor = self.__ns_collection.find({"name": name})
        print Cursor.count()
        if Cursor.count() != 0:
            self.__logger.debug("load ns entry (%s)" % name)
            NS_entry = Cursor.next()
        else:
            self.__logger.error("Faild to load ns entry (%s)" % name)
            return -1
        
        Cursor = self.__tenant_collection.find({"name": NS_entry["tenant"]})
        if Cursor.count() == 0:
            self.__logger.warn("Tenant is empty (%s)" % name)
            NS_entry["tenant"] = "default"
        
        Cursor = self.__EP_collection.find({"name": NS_entry["ingress_endpoint"]})
        if Cursor.count() == 0:
            self.__logger.error("ingress_endpoint is missing")
            return -1
        
        Cursor = self.__EP_collection.find({"name": NS_entry["egress_endpoint"]})
        if Cursor.count() == 0:
            self.__logger.error("egress_endpoint is missing")
            return -1
        
        self.__logger.info("A network scenario check is complete")
        return 0
    
    def find_service_path(self, ingress_endpoint, egress_endpoint, VNFFG):
        """"Find service path from ingress endpoint to egress enpoint including serfice function chaining path
        :param     ingress_endpoint   :    The end point where traffic is ingress
        :param     egress_endpoint    :    The end point where traffic is egress
        :param     VNFFG           :    The service function list that traffics will be passed
        :return    service_path       :    the list of service path inclouding attached 
        """
        service_path = []
        
        print ingress_endpoint
        
        port = ingress_endpoint["attached_switch"]["attached_port"]
        dpid = ingress_endpoint["attached_switch"]["dpid"]
        
        source = {"dpid": dpid, "port": port}
        
        destination = ""
        
        print "source         : %s" % source
        print "destination    : %s" % destination
        print "VNFG %s " % VNFFG
        
        if VNFFG != None:
            # print self.__VNFFG_collection[NS_entry["VNFFG"]]
            print "1"
            for sf in VNFFG["sf_list"]:
                print "2"
                # print "service function  : %s" % sfc
                # print "detail            : %s" % SF_collection[sfc]
                print "3"
                print sf
                sff_connection_info = self.find_service_function_forwarder(sf)
                print "4"
                
                
                if sff_connection_info == None:
                    print "cannot find correct service function forwarder"
                    return None
                
                # print sff_connection_info
                destination = {"port":sff_connection_info["attach_info"]["ingress_port"], "dpid":sff_connection_info["dpid"]}
                 
                
                # print destination
                print "PATH Info: Src SW DPID: %s, Src SW port: %s, Dest SW DPID: %s, Dest SW port: %s" % (source["dpid"], source["port"], destination["dpid"], destination["port"])
                service_path_entry = self.OFhandler.get_route(source["dpid"], source["port"], destination["dpid"], destination["port"])
                
                if not service_path_entry :
                    self.__logger.error("there are no service_path_entry %s" % service_path_entry)
                    return None
                else:
                    service_path = service_path + service_path_entry
                
                source = {"port":sff_connection_info["attach_info"]["egress_port"], "dpid":sff_connection_info["dpid"]}
                
        else:
            print "There is not a list of service function chaning"
            VNFFG = ""
        
        destination = {"port": egress_endpoint["attached_switch"]["attached_port"],
                        "dpid": egress_endpoint["attached_switch"]["dpid"]}
        
        
        service_path_entry = self.OFhandler.get_route(source["dpid"], source["port"], destination["dpid"], destination["port"])
        print "service_path_entry %s" % service_path_entry
        if not service_path_entry:
            self.__logger.error("service_path_entry %s" % service_path_entry)
            return -1
        else:
            service_path = service_path + service_path_entry
                
        print "PATH Info: Src SW DPID: %s, Src SW port: %s, Dest SW DPID: %s, Dest SW port: %s" % (source["dpid"], source["port"], destination["dpid"], destination["port"])
        pprint.pprint(service_path)   
        
        return service_path
    
    def rendor_floodlight_static_pusher_json(self, name, service_path):
        """Rendor the service path to JSON formet for static flow pusher to reflect the tenant setting.
        :param     name       :    The name of Service Function Path
        :param     service_path   :    The list of Service Path
        :param     tenant         :    The setting of tenant (e.g., src IP 10.0.0.0/24 UDP Traffic, arp apckets)
        :return    renderd_path   :    the list of Json data for static flow pusher
        """
        
        NS_entry = ''
        Cursor = self.__ns_collection.find({"name": name})
        print Cursor.count()
        if Cursor.count() != 0:
            self.__logger.debug("load ns entry (%s)" % name)
            NS_entry = Cursor.next()
            
        print NS_entry
        tenant = ''
        Cursor = self.__tenant_collection.find({"name": NS_entry['tenant']})
        print Cursor.count()
        if Cursor.count() != 0:
            self.__logger.debug("load tenant entry (%s)" % name)
            tenant = Cursor.next()
        
        
        renderd_path = {}
        renderd_path['general'] = []
        renderd_path['dasan'] = []
        
        print "123"
         
        for of_num in range (0, len(service_path) / 2):
            print "rendering service_path entry"
            
            src_ep = service_path[2 * of_num]
            print "src ep %s" % src_ep
            dest_ep = service_path[2 * of_num + 1]
            print "dest ep %s" % dest_ep
            
            print "src_ep DPID: %s" % src_ep["switch"]
            print "Tenant Name: %s" % (tenant)
            print tenant["attributes"]
            
            if self.__SFF_collection[src_ep["switch"]]["type"] == "dasan" :
                json = {
                      "flow_mod": {
                        "_name": "%s_%s_%s" % (name, tenant["name"], of_num),
                        "_description": "Description",
                        "#comments": "Comments",
                        "table": "acl",
                        "cmd": "add",
                        "mask": "0",
                        "port": "any",
                        "group": "any",
                        "priority": "100",
                        "match": {
                          "in_port": src_ep["port"]["shortPortNumber"],
                        },
                        "instructions": [
                          {
                            "write": [
                              {
                                "actions": [
                                  {
                                    "group": {
                                      "group_id": "0x%05X" % (dest_ep["port"]["shortPortNumber"])
                                    }
                                  }
                                ]
                              }
                            ]
                          }
                        ]
                      }
                    }
                
                for (key, value) in tenant["attributes"].items():
                    json["match"][key] = value
                
                path = {}
                path["dpid"] = src_ep["switch"]
                path["json"] = json
                
                renderd_path['dasan'].append(path)
                
                json_reverse = {
                      "flow_mod": {
                        "_name": "%s_%s_%s" % (name, tenant["name"], of_num),
                        "_description": "Description",
                        "#comments": "Comments",
                        "table": "acl",
                        "cmd": "add",
                        "mask": "0",
                        "port": "any",
                        "group": "any",
                        "priority": "100",
                        "match": {
                          "in_port": dest_ep["port"]["shortPortNumber"],
                        },
                        "instructions": [
                          {
                            "write": [
                              {
                                "actions": [
                                  {
                                    "group": {
                                      "group_id": "0x%05X" % (src_ep["port"]["shortPortNumber"])
                                    }
                                  }
                                ]
                              }
                            ]
                          }
                        ]
                      }
                    }
                
                for (key, value) in tenant["attributes"].items():
                    json_reverse["match"][key] = value
                    
                path = {}
                path["dpid"] = src_ep["switch"]
                path["json"] = json_reverse
                
                renderd_path['dasan'].append(json)
            
            else:
                json = {
                     "switch":src_ep["switch"],
                     "name":"%s_%s_%s" % (name, tenant["name"], of_num),
                     "cookie":"0",
                     "priority":"100",
                     "in_port":src_ep["port"]["shortPortNumber"],
                     "active":"true",
                     "actions":"output=%s" % (dest_ep["port"]["shortPortNumber"])
                 }
                
                
                for (key, value) in tenant["attributes"].items():
                    json[key] = value
                
                renderd_path['general'].append(json)
                
                json_reverse = {
                     "switch":src_ep["switch"],
                     "name":"%s_%s_%s_reverse" % (name, tenant["name"], of_num),
                     "cookie":"0",
                     "priority":"100",
                     "in_port":dest_ep["port"]["shortPortNumber"],
                     "active":"true",
                     "actions":"output=%s" % (src_ep["port"]["shortPortNumber"])
                 }
                
                for (key, value) in tenant["attributes"].items():
                    json_reverse[key] = value
                pprint.pprint(json_reverse)
                renderd_path['general'].append(json_reverse)
        
        pprint.pprint(renderd_path)
        return renderd_path

    
    def find_service_function_forwarder(self, service_function_name):
        # find service fucntion forwarder (e.g., OVS, DASAN 1G OpenFlow, DASAN 10G OpenFlow) connected to the service function (SF)
        
        
#         Cursor = self.__SFF_collection.find({
#                                              "connected_sf":{
#                                                              "name":service_function_name
#                                                            }
#                                              })
        SFF_Cursor = self.__SFF_collection.find()
        
        
        count = SFF_Cursor.count()
        for i in range (0, count):
            sff = SFF_Cursor.next()
            if (service_function_name in sff["connected_sf"]):
                return {"dpid": sff["dpid"], "attach_info":sff["connected_sf"][service_function_name]}
                
            
            
        
#         for (dpid, sff_info) in self.__SFF_collection.items():
#             if (service_function_name in sff_info["connected_sf"]):
#                 return {"dpid": dpid, "attach_info":sff_info["connected_sf"][service_function_name]}
#         
        return None
    
    
    def deploy_rendored_service_path(self, renderd_path):
        # deploy rendored service path by using floodlight static flow pusher
        
        for json in renderd_path['general']:
            print self.OFhandler.static_flow_pusher_add(json)
        
        for path in renderd_path['dasan']:
            print self.OFhandler.dasan_flow_pusher_add(path['dpid'], path['json'])
        
        
    def clear_openflow_switches(self):
        self.OFhandler.static_flow_pusher_list('all')
        self.OFhandler.static_flow_pusher_clear('all')
        self.OFhandler.static_flow_pusher_list('all')
    
    
    def init_openflow_switches(self):
        switch_port_info = self.OFhandler.get_switch_port()
        self.OFhandler.static_flow_pusher_list('all')
        self.OFhandler.static_flow_pusher_clear('all')
        self.OFhandler.static_flow_pusher_list('all')
        
        for (key, value) in switch_port_info.items():
            print key
            for port in value["port"]:
                print port["portNumber"]
                self.OFhandler.static_flow_pusher_add({
                                                "switch":key,
                                                "name":"%s port drop rule" % (port["portNumber"]),
                                                "cookie":"0",
                                                "priority":"1",
                                                "in_port":port["portNumber"],
                                                "active":"true",
                                                "actions":"output=drop"
                                            })
    
    def openflow_switch_flow_list(self):
        # switch_flow_info = self.OFhandler.get_switch_flow()
        switch_flow_info = self.OFhandler.static_flow_pusher_list("all")
        pprint.pprint(switch_flow_info)
            

# SFCManager = SFCManager()
# SFCManager.show_service_path(ns_collection["ns_dict_1"])
# SFCManager.validate_NS(ns_collection["ns_dict_1"])
# SFCManager.find_service_function_path(ns_collection["ns_dict_1"])

# 1st Testing
# SFCManager = SFCManager()
# SFCManager.init_openflow_switches()
# SFCManager.openflow_switch_flow_list()

# 2nd Testing
# SFCManager = SFCManager()
# SFCManager.init_openflow_switches()

# 1st
# renderd_path = SFCManager.find_service_function_path(ns_collection["ns_dict_0"])

# 2nd
# renderd_path = SFCManager.find_service_function_path(ns_collection["ns_dict_1"])

# 3rd
# renderd_path = SFCManager.find_service_function_path(ns_collection["ns_dict_2"])
# 4th
# renderd_path = SFCManager.find_service_function_path(ns_collection["ns_dict_3"])
# 5th
# renderd_path = SFCManager.find_service_function_path(ns_collection["ns_dict_4"])
# 6th
# renderd_path = SFCManager.find_service_function_path(ns_collection["ns_dict_5"])
# 6th
# renderd_path = SFCManager.find_service_function_path(ns_collection["ns_dict_6"])

# 7th
# renderd_path = SFCManager.find_service_function_path(ns_collection["ns_dict_7"])

# 8th
# renderd_path = SFCManager.find_service_function_path(ns_collection["ns_dict_8"])

# 9th
# renderd_path = SFCManager.find_service_function_path(ns_collection["ns_dict_9"])

# 10th
# renderd_path = SFCManager.find_service_function_path(ns_collection["ns_dict_10"])


# SFCManager.deploy_rendored_service_path(renderd_path)
# SFCManager.openflow_switch_flow_list()
