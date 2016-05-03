'''
Created on Dec 14, 2015

@author: root
'''

import logging
from neutronclient.neutron import client
import pprint


logging.basicConfig(level=logging.DEBUG)
neutron = client.Client('2.0', endpoint_url='http://192.168.17.179:9696', username="admin", password="jung1541", tenant_name="admin", auth_url='http://192.168.17.179:5000/v2.0')
networks = neutron.list_networks()
pprint.pprint(networks)
ports = neutron.list_ports()

# neutron.
pprint.pprint(ports)

# network_id = networks['networks'][0]['id']
# neutron.delete_network(network_id)
