# '''
# Created on Dec 14, 2015
# 
# @author: root
# '''
# from keystoneclient.auth.identity import v2
# from keystoneclient import session
# from novaclient import client
# 
# auth = v2.Password(auth_url="http://192.168.17.179:35357/v2.0",
#                     username="admin",
#                     password="jung1541",
#                     tenant_name="admin")
# sess = session.Session(auth=auth)
# nova = client.Client("3", session=sess)
# list = nova.servers.list()
# print list