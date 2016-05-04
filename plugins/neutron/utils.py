'''
Created on May 1, 2016

@author: root
'''
def print_values(val, type):
    if type == 'ports':
        val_list = val['ports']
    if type == 'networks':
        val_list = val['networks']
    if type == 'routers':
        val_list = val['routers']
    for p in val_list:
        for k, v in p.items():
            print("%s : %s" % (k, v))
        print('\n')


def print_values_server(val, server_id, type):
    if type == 'ports':
        val_list = val['ports']

    if type == 'networks':
        val_list = val['networks']
    for p in val_list:
        bool = False
        for k, v in p.items():
            if k == 'device_id' and v == server_id:
                bool = True
        if bool:
            for k, v in p.items():
                print("%s : %s" % (k, v))
            print('\n')
            
            
def print_flavors(flavor_list):
    for flavor in flavor_list:
        print("-"*35)
        print("flavor id : %s" % flavor.id)
        print("flavor name : %s" % flavor.name)
        print("-"*35)
       

def print_ports(val):
    port_list = val['ports']
    for port in port_list:
        print("-"*35)
        print "status: %s" % port["status"]
        print "binding:host_id: %s" % (port["binding:host_id"])
        print "name: %s" % (port["name"])
        print "allowed_address_pairs: %s" % (port["allowed_address_pairs"])
        print "admin_state_up: %s" % (port["admin_state_up"])
        print "network_id: %s" % (port["network_id"])
        print "tenant_id: %s" % (port["tenant_id"])
        print "extra_dhcp_opts: %s" % (port["extra_dhcp_opts"])
        print "mac_address: %s" % (port["mac_address"])
        print "binding:vif_details: %s" % (port["binding:vif_details"])
        print "binding:vif_type: %s" % (port["binding:vif_type"])
        print "device_owner: %s" % (port["device_owner"])
        print "binding:profile: %s" % (port["binding:profile"])
        print "port_security_enabled: %s" % (port["port_security_enabled"])
        print "binding: %s" % (port["binding:vnic_type"])
        print "fixed_ips: %s" % (port["fixed_ips"])
        print "id: %s" % (port["id"])
        print "security_groups: %s" % (port["security_groups"])
        print "device_id: %s" %(port["device_id"])
        print("-"*35)


def print_hosts(host_list):
    for host in host_list:
       print("-"*35)
       print("host_name : %s" % host.host_name)
       print("service : %s" % host.service)
       print("zone : %s" % host.zone)
       print("-"*35)
       

def print_hypervisors(hypervisor_list):
    for hypervisor in hypervisor_list:
       print("-"*35)
       print("id : %s" % hypervisor.id)
       print("status : %s" % hypervisor.status)
#        print("service : %s" % hypervisor.service)
#        print("vcpus_used : %s" % hypervisor.vcpus_used)
#        print("hypervisor_type : %s" % hypervisor.hypervisor_type)
#        print("local_gb_used : %s" % hypervisor.local_gb_used)
#        print("vcpus : %s" % hypervisor.vcpus)
       print("hypervisor_hostname : %s" % hypervisor.hypervisor_hostname)
#        print("memory_mb_used : %s" % hypervisor.memory_mb_used)
#        print("memory_mb : %s" % hypervisor.memory_mb)
#        print("current_workload : %s" % hypervisor.current_workload)
#        print("state : %s" % hypervisor.state)
       print("host_ip : %s" % hypervisor.host_ip)
#        print("cpu_info : %s" % hypervisor.cpu_info)
       print("running_vms : %s" % hypervisor.running_vms)
#        print("free_disk_gb : %s" % hypervisor.free_disk_gb)
#        print("hypervisor_version : %s" % hypervisor.hypervisor_version)
#        print("disk_available_least : %s" % hypervisor.disk_available_least)
#        print("local_gb : %s" % hypervisor.local_gb)
#        print("free_ram_mb : %s" % hypervisor.free_ram_mb)
       print("-"*35)
       