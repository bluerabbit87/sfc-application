# '''
# Created on Dec 14, 2015
# 
# @author: root
# '''

import collections
import json
import logging
import socket
import threading
from time import sleep

class OVSDBManager(object):
    '''
    classdocs
    '''
    def __init__(self, ip_, port_):
        '''
        Constructor
        '''
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip_, int(port_)))
         
    def query(self, json_data):
        self.s.send(json.dumps(json_data))
        result = ""
        while (True):
            response = self.s.recv(4096)
            result = result + response
            try:
                json_result = json.loads(result)
                return json_result
            except:
                print ""
             
    def listDB(self):
        listDB = {"method":"list_dbs", "params":[], "id": 0}
        return self.query(listDB)
     
    def getSchema(self):
        Get_Schema = {"method":"get_schema", "params":["Open_vSwitch"], "id": 0}
        return self.query(Get_Schema)
     
    def transact(self,params):
        Transact            =   {"method":"transact", "params":[], "id": 0}
        Transact["params"]  =   params
        return self.query(Transact)
     
    def monitor(self,params):
        Monitor             = {'id': 100, 'method': 'monitor', 'params': ""}
        Monitor["params"] = params
         
        return self.query(Monitor)
     
    def run(self):
        i=0
        while(True):
            sleep(1)
            result = ""
            while (True):
                response = self.s.recv(4096)
                result = result + response
                try:
                    json_result = json.loads(result)
                    print json_result
                    break
                except:
                    print ""
            print result




logging.basicConfig(level=logging.DEBUG)


OVSDB_IP = '192.168.17.179'
OVSDB_PORT = 6632

"""
a simple client to talk to ovsdb over json rpc
"""


def default_echo_handler(message, ovsconn):
    logging.debug("responding to echo")
    ovsconn.send({"result": message.get("params", None),
                  "error": None, "id": message['id']})

def default_message_handler(message, ovsconn):
    logging.debug("default handler called for method %s", message['method'])
    ovsconn.responses.append(message)

class OVSDBConnection(threading.Thread):
    """Connects to an ovsdb server that has manager set using
        ovs-vsctl set-manager ptcp:5000
        clients can make calls and register a callback for results, callbacks
         are linked based on the message ids.
        clients can also register methods which they are interested in by
        providing a callback.
    """

    def __init__(self, IP, PORT, **handlers):
        super(OVSDBConnection, self).__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((IP, PORT))
        self.responses = []
        self.callbacks = {}
        self.read_on = True
        self.handlers = handlers or {"echo": default_echo_handler}
        self.start()

    def send(self, message, callback=None):
        if callback:
            self.callbacks[message['id']] = callback
        self.socket.send(json.dumps(message))

    def response(self, id):
        return [x for x in self.responses if x['id'] == id]

    def set_handler(self, method_name, handler):
        self.handlers[method_name] = handler

    def _on_remote_message(self, message):
        logging.debug("message %s", message)
        try:
            json_m = json.loads(message,
                                object_pairs_hook=collections.OrderedDict)
            # check first to see if the message is for a method and we have a
            # handler for it
            handler_method = json_m.get('method', None)
            if handler_method:
                self.handlers.get(handler_method, default_message_handler)(
                    json_m, self)
            elif json_m.get("result", None) and json_m['id'] in self.callbacks:
                id = json_m['id']
                # check if this is a result of an earlier call we made and that
                # we have a callback registered
                if not self.callbacks[id](json_m, self):
                    # if callback is to be persisted, callback should return
                    # something
                    self.callbacks.pop(id)

            else:
                # add it for sync clients
                default_message_handler(message, self)
        except Exception as e:
            logging.exception("exception [%s] while handling message [%s]", e.message, message)

    def __echo_response(self, message):
        self.send({"result": message.get("params", None),
                   "error": None, "id": message['id']})

    def run(self):

        chunks = []
        lc = rc = 0
        while self.read_on:
            response = self.socket.recv(4096)
            if response:
                response = response.decode('utf8')
                message_mark = 0
                for i, c in enumerate(response):
                    # todo fix the curlies in quotes
                    if c == '{':
                        lc += 1
                    elif c == '}':
                        rc += 1

                    if rc > lc:
                        raise Exception("json string not valid")

                    elif lc == rc and lc is not 0:
                        chunks.append(response[message_mark:i + 1])
                        message = "".join(chunks)
                        self._on_remote_message(message)
                        lc = rc = 0
                        message_mark = i + 1
                        chunks = []

                chunks.append(response[message_mark:])

    def stop(self, force=False):
        self.read_on = False
        if force:
            self.socket.close()


