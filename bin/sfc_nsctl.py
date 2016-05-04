#!/usr/bin/env python
# encoding: utf-8

'''
__init__ -- shortdesc

__init__ is a description

It defines classes_and_methods

@author:     chiwook jeogn

@copyright:  2015 organization_name. All rights reserved.

@license:    license

@contact:    chiwook.jeong@kt.com
@deffield    updated: Updated
'''
import ConfigParser
import argparse
from atk import Document
from dbus.proxies import Interface
import json
import logging
import logging.handlers
from neutronclient.v2_0 import client
from novaclient.client import Client
from optparse import OptionParser, OptionGroup
import os
import pprint 
from pymongo import MongoClient
import sys

sys.path.append('../cores')
sys.path.append('../plugins')

from floodlight.floodlight_agent import OpenFlowHandler
from ietf_sfc import SFManager, SFFManager, EPManager, VNFFGManager, NSManager, \
    tenantManager, SFCManager
from openstack.credentials import get_credentials, get_nova_credentials_v2
from openstack.utils import print_ports, print_values, print_hypervisors
from ovsdb.OVSDBManager import OVSDBManager


__all__ = []
__version__ = 0.1
__date__ = '2015-10-22'
__updated__ = '2015-12-12'

DEBUG = 1
TESTRUN = 0
PROFILE = 0
# logger = ""

def load_config(logger):
    
    config = ConfigParser.ConfigParser();
    
    read_result = config.read('conf/config.conf')
    
    if (read_result == []):
        read_result = config.read('../conf/config.conf')
    
    if (read_result == []):
        print "Fail to read the configuration file"
        logger.critical("Fail to read the configuration file")
        config_dict = {}
        
        config_dict = {"MongoDB": {'ip':"127.0.0.1", 'port':27017},
                        'Log':     {'level':"DEBUG", 'STDOUT':"TRUE", 'location':"./sfc-nsctl.log"},
                        'Floodlight': {'level':"DEBUG", 'ip':"127.0.0.1", 'port':"8080"},
                        'ovsdb': {'ip':"192.168.43.3", 'port':"6632"}}
        
        return config_dict
    
    logger.info("Loading a configuration from a config file")
    
    config_dict = {}
    for section in config.sections():
        opt_dict = {};
        for option in config.options(section):
            try:
                opt_dict[option] = config.get(section, option)
                logger.debug ("Session: %s, config: %s, value: %s" % (section, option, opt_dict[option])) 
                
                if opt_dict[option] == -1:
                    logger.debug("skip: %s" % option)
            except:
                logger.debug("exception on %s!" % option)
                opt_dict[option] = None
                
        config_dict[section] = opt_dict
    
    logger.info("Configuration loading is finished")
    logger.debug("Config results: " + str(config_dict))
    
    return config_dict


def main(argv=None):
    '''Command line options.'''

    program_name = os.path.basename(sys.argv[0])
    program_version = "v0.1"
    program_build_date = "%s" % __updated__
    
    program_version_string = '%%prog %s (%s)' % (program_version, program_build_date)
    # program_usage = '''usage: spam two eggs''' # optional - will be autogenerated by optparse
    program_longdesc = ''''''  # optional - give further explanation about what the program does
    program_license = "Copyright 2015 user_name (organization_name)                                            \
                Licensed under the Apache License 2.0\nhttp://www.apache.org/licenses/LICENSE-2.0"

    
    logger = logging.getLogger('logger')
    
    # creates formatter 
    fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
#     consoleHandler = logging.StreamHandler()
#     consoleHandler.setFormatter(fomatter)
#     logger.addHandler(consoleHandler)
#     
         # 로거 인스턴스의 로깅 레벨을 설정한다.
    if DEBUG == 1:
        logger.setLevel("DEBUG")
    else:
        logger.setLevel("INFO")
        
        
    config = load_config(logger)
    fileHandler = logging.FileHandler(config['Log']['location'])
    fileHandler.setFormatter(fomatter)
    logger.addHandler(fileHandler)
    
    
    logger.setLevel(config['Log']['level'])
    mongoclient = MongoClient(config['MongoDB']['ip'],
                               int(config['MongoDB']['port']))
    
    sfc_db = mongoclient.sfc_database
    
    SFmanager = SFManager(sfc_db, logger)
    SFFmanager = SFFManager(sfc_db, logger)
    EPmanager = EPManager(sfc_db, logger)
    VNFFGmanager = VNFFGManager(sfc_db, logger)
    NSmanager = NSManager(sfc_db, logger)
    tenantmanager = tenantManager(sfc_db, logger)
    
    print config['ovsdb']['ip'],config['ovsdb']['port']
    OVSDBmanager    = OVSDBManager(config['ovsdb']['ip'],config['ovsdb']['port'])
    #ovsdb = OVSDBConnection(config['ovsdb']['ip'],int(config['ovsdb']['port']))
    
    OFhandler = OpenFlowHandler(config['Floodlight']['ip'], config['Floodlight']['port'])
    SFCmanager = SFCManager(OFHandler_=OFhandler, sfc_db=sfc_db, logger=logger)

    
    if argv is None:
        argv = sys.argv[1:]
    try:
        # setup option parser
        parser = OptionParser(version=program_version_string, epilog=program_longdesc, description=program_license, add_help_option=False)
        parser.add_option("-h", "--help", dest="help", action="store_true", help="show this help message and exit")
        
        parser.add_option("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %default]")
                  
        sf_group = OptionGroup(parser, "Detail options")
        sf_group.add_option("-n", "--name", dest="name", action="store", type="string", help="set a name")
        sf_group.add_option("-t", "--type", dest="type", action="store", type="string", help="set a type")
        sf_group.add_option("-i", "--ip", dest="ip", action="store", type="string", help="set a ip")
        sf_group.add_option("-p", "--port", dest="port", action="store", type="string", help="set a port")
        sf_group.add_option("-d", "--dpid", dest="dpid", action="store", type="string", help="set a dpid")
        sf_group.add_option("-j", "--json", dest="json", action="store", type="string", help="set a json data")
        
        sf_group.add_option("--network_scenario", dest="network_scenario", action="store", type="string", help="set a network scenario")
        sf_group.add_option("--ingress_endpoint", dest="ingress_endpoint", action="store", type="string", help="set a ingress_endpoint")
        sf_group.add_option("--egress_endpoint", dest="egress_endpoint", action="store", type="string", help="set a egress_endpoint")
        sf_group.add_option("--vnffg", dest="vnffg", action="store", type="string", help="set a vnffg")
        sf_group.add_option("--tenant", dest="tenant", action="store", type="string", help="set a tenant")
        sf_group.add_option("--priority", dest="priority", action="store", type="string", help="set a prioriry")
        sf_group.add_option("--attributes", dest="attributes", action="store_true", help="set a attributes")
        sf_group.add_option("--sf_lists", dest="sf_list", action="store_true", help="set a sf list")
        sf_group.add_option("--interface", dest="interfaces", action="store_true", help="set a interface info")
        sf_group.add_option("--connected_sfs", dest="connected_sfs", action="store_true", help="set a conncected sfs info")
        sf_group.add_option("--vlan", dest="vlan", action="store", type="string", help="set a vlan")
        
        parser.add_option_group(sf_group)
         
        # process options
        (opts, args) = parser.parse_args(argv)
        
        json_data = None
        if opts.json:
            with open(opts.json) as data_file:    
                json_data = json.load(data_file)
            
            # pprint.pprint(json_data)
            
        if args != []:
            command = args[0]
            if command == "create-sf":
                options = SFmanager.parse_args(opts.interfaces, 4, args)
                SFmanager.create_entry(json_data=json_data, name=opts.name, type=opts.type, ip=opts.ip, options=options)
            
            elif command == "list-sf":
                SFmanager.list_entry()
            
            elif command == "update-sf":
                interfaces = SFmanager.parse_args(opts.interfaces, args)
                SFmanager.update_entry(json_data=json_data, name=opts.name, type=opts.type, ip=opts.ip, interfaces=interfaces)
                
            elif command == "delete-sf":
                SFmanager.delete_entry(opts.name)
                
            elif command == "create-sff":
                print "create-sff"    
                options = SFFmanager.parse_args(opts.connected_sfs, 3, args)
                SFFmanager.create_entry(json_data=json_data, name=opts.name, dpid=opts.dpid, type=opts.type, options=options)
    
            elif command == "list-sff":
                SFFmanager.list_entry()
                 
            elif command == "update-sff":
                options = SFFmanager.parse_args(opts.connected_sfs, 3, args)
                SFFmanager.update_entry(json_data=json_data, name=opts.name, dpid=opts.dpid, type=opts.type, options=options)
    
            elif command == "delete-sff":
                SFFmanager.delete_entry(opts.name)
                
            elif command == "create-ep":
                EPmanager.create_entry(json_data=json_data, name=opts.name, vlan=opts.vlan, dpid=opts.dpid, port=opts.port)
                
            elif command == "list-ep":
                EPmanager.list_entry()
                
            elif command == "update-ep":
                EPmanager.update_entry(json_data=json_data, name=opts.name, vlan=opts.vlan, dpid=opts.dpid, port=opts.port)
    
            elif command == "delete-ep":
                EPmanager.delete_entry(opts.name)
            
            elif command == "create-tenant":
                options = tenantmanager.parse_args(opts.attributes, args)
                tenantmanager.create_entry(json_data=json_data, name=opts.name, priority=opts.priority, attributes=options)

            elif command == "list-tenant":
                tenantmanager.list_entry()
            
            elif command == "update-tenant":
                options = tenantmanager.parse_args(opts.attributes, args)
                tenantmanager.update_entry(json_data=json_data, name=opts.name, priority=opts.priority, attributes=options)

            elif command == "delete-tenant":
                tenantmanager.delete_entry(opts.name)
                
            elif command == "create-vnffg":
                options = VNFFGmanager.parse_args(opts.sf_list, args)
                VNFFGmanager.create_entry(json_data=json_data, name=opts.name, sf_list=options)

            elif command == "list-vnffg":
                VNFFGmanager.list_entry()

            elif command == "update-vnffg":
                options = VNFFGmanager.parse_args(opts.sf_list, args)
                VNFFGmanager.update_entry(json_data=json_data, name=opts.name, sf_list=options)

            elif command == "delete-vnffg":
                VNFFGmanager.delete_entry(name=opts.name)
                
            elif command == "create-ns":
                NSmanager.create_entry(json_data=json_data, name=opts.name, ingress_endpoint=opts.ingress_endpoint, egress_endpoint=opts.egress_endpoint, vnffg=opts.vnffg, tenant=opts.tenant)

            elif command == "list-ns":
                NSmanager.list_entry()

            elif command == "update-ns":
                NSmanager.update_entry(json_data=json_data, name=opts.name, ingress_endpoint=opts.ingress_endpoint, egress_endpoint=opts.egress_endpoint, vnffg=opts.vnffg, tenant=opts.tenant)

            elif command == "delete-ns":
                NSmanager.delete_entry(name=opts.name)
            
            elif command == "show-ns":
                SFCmanager.show_service_path(name=opts.name)
            
            elif command == "check-ns-available":
                SFCmanager.validate_NS(name=opts.name)
                
            elif command == "find-service-function-path":
                service_path = SFCmanager.find_service_function_path(name=opts.name)
                print service_path
                
            elif command == "rendor-openflow-json":
                service_path = SFCmanager.find_service_function_path(name=opts.name)
                rendered_path = SFCmanager.rendor_floodlight_static_pusher_json(name=opts.name, service_path=service_path)
                
            elif command == "install-ns":
                service_path = SFCmanager.find_service_function_path(name=opts.name)
                rendered_path = SFCmanager.rendor_floodlight_static_pusher_json(name=opts.name, service_path=service_path)
                
                SFCmanager.deploy_rendored_service_path(rendered_path)
                SFCmanager.openflow_switch_flow_list()
                
#         return rendered_path

#                 SFCmanager.deploy_rendored_service_path(renderd_path)
#                 
            
            
            elif command == "status-ns":
                SFCmanager.openflow_switch_flow_list()
                
            elif command == "clear-ns":
                SFCmanager.clear_openflow_switches()

            elif command == "init-ns":
                SFCmanager.init_openflow_switches()
            
            elif command == "list-ovs-bridge":
                result = OVSDBmanager.transact(["Open_vSwitch",{"op":"select","table":"Bridge","where":[]}])
                pprint.pprint(result)
#               
            elif command == "list-ovs-interface":
                result = OVSDBmanager.transact(["Open_vSwitch",{"op":"select","table":"Interface","where":[]}])
                pprint.pprint(result)
            
            elif command == "list-ovs-port":
                result = OVSDBmanager.transact(["Open_vSwitch",{"op":"select","table":"Port","where":[]}])
                pprint.pprint(result)
            
            elif command == "list-ovs-controller":
                result = OVSDBmanager.transact(["Open_vSwitch",{"op":"select","table":"Controller","where":[]}])
                pprint.pprint(result)

            elif command == "list-neutron-port":
                credentials = get_credentials()
                neutron = client.Client(**credentials)
                ports = neutron.list_ports()
                print_ports(ports)
            
            elif command == "list-neutron-network":
                credentials = get_credentials()
                neutron = client.Client(**credentials)
                netw = neutron.list_networks()
                print_values(netw, 'networks')
                
            elif command == "list-nova-hypervisor":
                credentials = get_nova_credentials_v2()
                nova_client = Client(**credentials)
                
                hypervisor_id_list = nova_client.hypervisors.list()
                print_hypervisors(hypervisor_id_list)
                for hypervisor_id in hypervisor_id_list:
                    print nova_client.hypervisors.get(hypervisor_id)
                
            elif command == "ovsdb-testing":
                # E.g setting a callback and making a call. Note that the callback has to
                # set everytime unless the callback returns a truth value (True)
                def res(message, ovsconn):
                    print "list_dbs_query response ", json.dumps(message)
            
                # #with callback
                list_dbs_query = {"method": "get_schema", "params": ['Open_vSwitch'],
                                  "id": 0}
                #ovsdb.send(list_dbs_query, res)
            
                def monitor_res(message, ovsconn):
                    print "monitor response", json.dumps(message)
                    return True  # we want to persist this callback
            
                monitor_message = {'id': 100, 'method': 'monitor', 'params': ['Open_vSwitch', None, {
                    'Bridge': [{'select': {'initial': True, 'insert': True, 'delete': True,
                                           'modify': True}}]}]}
                #ovsdb.set_handler("update", monitor_res)
                #ovsdb.send(monitor_message, monitor_res)
                
                result = OVSDBmanager.transact(["Open_vSwitch",{"op":"select","table":"Interface","where":[]}])
                pprint.pprint(result)
#                 
#                 result = OVSDBmanager.listDB()
#                 pprint.pprint(result)
#                 
#                 
#                 result = OVSDBmanager.getSchema()
#                 pprint.pprint(result)
# 
#                   result = OVSDBmanager.monitor(['Open_vSwitch', 10, {
#                                                                                                  'Interface': [{'select': 
#                                                                                                              {'initial': True, 
#                                                                                                               'insert': True, 
#                                                                                                               'delete': True,
#                                                                                                              'modify': True}}]}])
#                   pprint.pprint(result)
#                   OVSDBmanager.run()

                
            else:
                print "unknown command '%s'; use --help or -h for help" % args[0]
            
        # if DEBUG:
            # print (opts, args)
            
        if opts.help:
            parser.print_help()
            
            print "Command lists:" 
            print "" 
            
            print "%s %s" % ("create-sf".ljust(20), "create a service function".ljust(20))
            print "%s %s" % ("list-sf".ljust(20), "list a service function".ljust(20))
            print "%s %s" % ("update-sf".ljust(20), "update a service function".ljust(20))
            print "%s %s" % ("delete-sf".ljust(20), "delete a service function".ljust(20))
            print ""
            
            print "%s %s" % ("create-sff".ljust(20), "create a service function forwarder".ljust(20))
            print "%s %s" % ("list-sff".ljust(20), "list a service function forwarder".ljust(20))
            print "%s %s" % ("update-sff".ljust(20), "update a service function forwarder".ljust(20))
            print "%s %s" % ("delete-sff".ljust(20), "delete a service function forwarder".ljust(20))
            print ""
            
            print "%s %s" % ("create-ep".ljust(20)  , "create a end point".ljust(20))
            print "%s %s" % ("list-ep".ljust(20)    , "list a end point".ljust(20))
            print "%s %s" % ("update-ep".ljust(20)  , "update a end point".ljust(20))
            print "%s %s" % ("delete-ep".ljust(20)  , "delete a end point".ljust(20))
            print ""
            
            
            print "%s %s" % ("create-tenant".ljust(20), "create a tenant".ljust(20))
            print "%s %s" % ("list-tenant".ljust(20), "list a tenant".ljust(20))
            print "%s %s" % ("update-tenant".ljust(20), "update a tenant".ljust(20))
            print "%s %s" % ("delete-tenant".ljust(20), "delete a tenant".ljust(20))
            print ""
            

            print "%s %s" % ("create-vnffg".ljust(20), "create a VNF forwarding graph".ljust(20))
            print "%s %s" % ("list-vnffg".ljust(20), "list a VNF forwarding graph".ljust(20))
            print "%s %s" % ("update-vnffg".ljust(20), "update a VNF forwarding graph".ljust(20))
            print "%s %s" % ("delete-vnffg".ljust(20), "delete a VNF forwarding graph".ljust(20))
            print ""
            

            print "%s %s" % ("create-ns".ljust(20), "create a network scenario".ljust(20))
            print "%s %s" % ("list-ns".ljust(20), "list a network scenario".ljust(20))
            print "%s %s" % ("update-ns".ljust(20), "update a network scenario".ljust(20))
            print "%s %s" % ("delete-ns".ljust(20), "delete a network scenario".ljust(20))
            print ""
            
            
            print "%s %s" % ("show-ns".ljust(20), "show the service path".ljust(20))
            print "%s %s" % ("check-ns-available".ljust(20), "check available of the network scenario".ljust(20))
            print "%s %s" % ("install-ns".ljust(20), "install the network scenario".ljust(20))
            print "%s %s" % ("uninstall-ns".ljust(20), "uninstall the deployed network scenario".ljust(20))
            print "%s %s" % ("status-ns".ljust(20), "show the status of the installed network scenario".ljust(20))
            print "%s %s" % ("clear-ns".ljust(20), "clear installed network scenario".ljust(20))
            
            
    
            return 2
        
        if opts.verbose > 0:
            print("verbosity level = %d" % opts.verbose)

             
        # MAIN BODY #
 
    except Exception, e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2
    

if __name__ == "__main__":
#    if DEBUG:
#        sys.argv.append("-h")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = '__init___profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
