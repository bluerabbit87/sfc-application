'''
Created on May 1, 2016

@author: root
'''
from novaclient.client import Client

from credentials import get_nova_credentials_v2
from utils import print_hypervisors
from utils import print_flavors
from utils import print_hosts


credentials = get_nova_credentials_v2()
nova_client = Client(**credentials)

# flavors_list = nova_client.flavors.list()
# print_flavors(flavors_list)
# 
# host_list = nova_client.hosts.list()
# print_hosts(host_list)

# hypervisor_id_list = nova_client.hypervisors.list()
# print_hypervisors(hypervisor_id_list)
# for hypervisor_id in hypervisor_id_list:
#     print nova_client.hypervisors.get(hypervisor_id)

print(nova_client.servers.list())