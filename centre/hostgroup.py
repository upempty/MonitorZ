#-*- coding: utf-8 -*-
import sys

def hostgroup_get2(zapi, name):
    param = {
        "filter": {
          "name": [name,]
        }
    }
    all2 = zapi.do_request('hostgroup.get', param)
    #print ("all2 group get", all2)
    groupid = all2['result'][0]['groupid']
    print ('gid:', groupid,sys._getframe().f_code.co_name)
    return (groupid)
'''
class HostGroup:
    def __init__(self, zapi):
        self.__zapi = zapi
        print(zapi)
    
    def hostgroup_get(self, name):
        param = {
            "filter": {
              "name": [name,]
            }
        }
        all2 = self.__zapi.do_request('hostgroup.get', param)
        #print ("all2 group get", all2)
        groupid = all2['result'][0]['groupid']
        print ('gid:', groupid,sys._getframe().f_code.co_name)
        return (groupid)

'''
