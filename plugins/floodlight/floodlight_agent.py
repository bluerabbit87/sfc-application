# encoding: utf-8
'''
Created on May 2, 2016

@author: root
'''
# -*- coding: utf-8 -*-
'''
Created on Sep 23, 2015

@author: bluerabbit87
'''

import cStringIO
import json
import logging
import pycurl
from urllib import urlencode


class OpenFlowHandler(object):
    ''' classdocs
    본 클래스는 Floodlgiht v1.1으로 부터 SDN 제어기의 상태, OpenFlow 스위치들의 상태를 
Floodlgiht에서 제공하는 아래의 RestAPI들을 호출하여 불러오는, 그리고 불러와서 Parsing
하는 역활을 합니다. 

Example: 

Request: http://127.0.0.1:8080/wm/core/switch/all/desc/json

Respond: 
 
{"00:00:00:00:00:00:00:03":{"desc":{"version":"OF_10","manufacturerDescription":
"Nicira Networks, Inc.","hardwareDescription":"Open vSwitch","softwareDescription":
"1.4.6","serialNumber":"None","datapathDescription":"None"}},"00:00:00:00:00:00:00:02
...
":"Nicira Networks, Inc.","hardwareDescription":"Open vSwitch","softwareDescription":"1.4.6",
"serialNumber":"None","datapathDescription":"None"}},"00:00:00:00:00:00:00:06":{"desc":{"}}}
    '''
    
    "Floodlight REST API URLs"
    url_switch_desc = '/wm/core/switch/all/desc/json'
    url_switch_port = '/wm/core/switch/all/port/json'
    url_switch_flow = '/wm/core/switch/all/flow/json'
    url_topology_link = '/wm/topology/links/json'
    url_device = '/wm/device'
    url_route = '/wm/topology/route'
    url_static_flow_pusher = '/wm/staticflowpusher/json'

    def __init__(self, controller_ip, controller_port, logger=None): 
        '''
        Constructor
        A __init__ function receives connection information of SDN controller such as IP and Port addresses.
        FloodlightPlugin communicates with SND controller with above IP and Port addresses.
        '''
        
        self.__controller_ip = controller_ip;
        self.__controller_port = controller_port;
        if logger == None:
            self.logger = logging.getLogger('logger');
            fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
        
            streamHandler = logging.StreamHandler();
            streamHandler.setFormatter(fomatter);
            self.logger.addHandler(streamHandler);
                
                        # 로거 인스턴스의 로깅 레벨을 설정한다.
            fileHandler = logging.FileHandler("./OpenflowHendler.log");
            fileHandler.setFormatter(fomatter);
            self.logger.addHandler(fileHandler);
        
            self.logger.setLevel("DEBUG");
        else:
            self.logger = logger;
        # At this time, FloodlightPlugin communicates with Floodlight via a pycurl library
        
    def get_controller_ip(self):
        # Return the IP address of sdn controller  
        return self.__controller_ip
    
    def get_controller_port(self):
        # Return a Port address of this FloodlightPlugin  
        return self.__controller_port
    
    def get_route(self, src_switch_DPID, src_switch_port, dest_switch_DPID, dest_switch_port):
        url = self.url_route
        route_request_url = "%s/%s/%s/%s/%s/json" % (self.url_route, src_switch_DPID, src_switch_port, dest_switch_DPID, dest_switch_port)
        print route_request_url
        return self.__get(route_request_url)
    
    def static_flow_pusher_add(self, post_data):
        self.__post(self.url_static_flow_pusher, post_data)
    
    def static_flow_pusher_list(self, switch_dpid):
        return self.__get("/wm/staticflowpusher/list/%s/json" % (switch_dpid))
        
    def static_flow_pusher_clear(self, switch_dpid):
        return self.__get("/wm/staticflowpusher/clear/%s/json" % (switch_dpid))
    
    def __post(self, url, post_data):
        # by using pycurl, __get function returns the response of the requested url.   
        self.logger.info("by using pycurl, __get function returns the response of the requested url.");
        local_pycurl = pycurl.Curl()
        
        request_curl_url = "http://" + self.__controller_ip + ":" + self.__controller_port + url
        local_pycurl.setopt(local_pycurl.URL, request_curl_url)
        self.logger.debug("request_curl_url: " + request_curl_url);
                
        local_pycurl.setopt(pycurl.HTTPHEADER, ['X-Postmark-Server-Token: API_TOKEN_HERE', 'Accept: application/json'])
        local_pycurl.setopt(pycurl.POST, 1)
        
        data = json.dumps(post_data)
        local_pycurl.setopt(pycurl.POSTFIELDS, data)
        self.logger.debug("request_curl_post_data: " + data);
                
        
        buf = cStringIO.StringIO()
        local_pycurl.setopt(local_pycurl.WRITEFUNCTION, buf.write)
        
        try:
            local_pycurl.perform()
            local_pycurl.close()
        except pycurl.error:
            self.logger.critical("couldn't connect to host");
            return None
       
        raw_json_response = buf.getvalue()
        buf.close()
        
        # by using json library, it parses recieved raw json data to python data structure (e.g., list, dictionary)  
        json_response = json.loads(raw_json_response);
        self.logger.debug(json.dumps(json_response, sort_keys=True,
                         indent=4, separators=(',', ': ')));
        return json_response
       
    def __get(self, url):
        # by using pycurl, __get function returns the response of the requested url.   
        self.logger.info("by using pycurl, __get function returns the response of the requested url.");
        local_pycurl = pycurl.Curl()   
        buf = cStringIO.StringIO()
        request_curl_url = "http://" + self.__controller_ip + ":" + self.__controller_port + url
        self.logger.debug("request_curl_url: " + request_curl_url);
        local_pycurl.setopt(local_pycurl.URL, request_curl_url)
        local_pycurl.setopt(local_pycurl.WRITEFUNCTION, buf.write)
        try:
            local_pycurl.perform()
            local_pycurl.close()
        except pycurl.error:
            self.logger.critical("couldn't connect to host");
            return None
            
        
        raw_json_response = buf.getvalue()
        buf.close()
        # by using json library, it parses recieved raw json data to python data structure (e.g., list, dictionary)  
        if raw_json_response != "":
            json_response = json.loads(raw_json_response);
            self.logger.debug(json.dumps(json_response, sort_keys=True,
                             indent=4, separators=(',', ': ')));
            return json_response
        
        else:
            self.logger.debug("There is no route for request info");
            return None
        
        
    def get_switch_desc(self):
        self.logger.info("get_switch_desc");
        return self.__get(self.url_switch_desc)
    
    def get_switch_port(self):
        self.logger.info("get_switch_port");
        return self.__get(self.url_switch_port)
    
    def get_switch_flow(self):
        self.logger.info("get_switch_flow");
        return self.__get(self.url_switch_flow)
        
    def get_topology_link(self):
        self.logger.info("get_topology_link");
        return self.__get(self.url_topology_link)
        
    def get_device(self):
        self.logger.info("get_device");
        return self.__get(self.url_device)
    
    def get(self, url):
        return self.__get(url)
    
    def port(self, url, post_data):
        return self.__post(url, post_data)
