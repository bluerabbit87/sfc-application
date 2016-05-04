'''
Created on May 1, 2016

@author: root
'''
from neutronclient.v2_0 import client
import pprint

from credentials import get_credentials
from utils import print_ports
from utils import print_values


credentials = get_credentials()
neutron = client.Client(**credentials)
# netw = neutron.list_networks()
# print_values(netw, 'networks')

ports = neutron.list_ports()
#print_values(ports,"ports")
print_ports(ports)

