'''
Created on May 3, 2016

@author: root
'''

if __name__ == '__main__':
    from paramiko import SSHClient,AutoAddPolicy
    client = SSHClient()                                                            
    client.load_system_host_keys()       
    client.set_missing_host_key_policy(AutoAddPolicy()) 
    
    client.connect('192.168.43.3', username='root', password='crazy_222')           
    stdin, stdout, stderr = client.exec_command('ip netns')                             
                                                                                   
#     for line in stdout:                                                             
#         print '... ' + line.strip('\n')   
#     
# 
#     stdin, stdout, stderr = client.exec_command('ifconfig')                             
#     for line in stdout:                                                             
#         print '... ' + line.strip('\n')   
#         
#     stdin, stdout, stderr = client.exec_command('ip a')                             
#     for line in stdout:                                                             
#         print '... ' + line.strip('\n')   
#         
    stdin, stdout, stderr = client.exec_command('iptables --list')                             
    for line in stdout:                                                             
        print '... ' + line.strip('\n')   
    
    
    
    pass
