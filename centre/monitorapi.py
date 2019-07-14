#!/usr/bin/env python
#-*- coding: utf-8 -*-

#from zabbixlib import ZabbixAPI
import sys
from centre.zabbixlib import ZabbixAPI
from centre.configs import *
from centre.hostgroup import *
#import *.....

#loging, class module, testing, items for monitors, exception handling

zapi = ZabbixAPI(Zserver)
zapi.login(Zusername, Zpassword)
print ("Connected ZAPI version %s" % zapi.api_version())


#Class MonitorAPI:
class MonitorAPI:
    def __init__(self, zapi):
        self.__zapi = zapi
        #self.hg = HostGroup(zapi)
        print ('MonitorAPI init invoked')
    
    def hostgroup_get(self, name):
        print ('hostgrup get 000start')
        #self.hg.hostgroup_get(name)
        hostgroup_get2(self.__zapi, name)
        print ('hostgrup get 000end')

    #some combine function 
    def create_host_item_on_template(self):
        pass
  

#create global instance for API usage
monitorAPI = MonitorAPI(zapi)



#gid = monitorAPI.hostgroup_get('CF_Group713')
#monitor = MonitorAPI()


'''
[{u'internal': u'0', u'flags': u'0', u'groupid': u'16', u'name': u'CF DB Srv1'}
'''
def hostgroup_create(name):
    param = {
        "name": name 
    }
    all = zapi.do_request('hostgroup.create', param)
    print (all['result']['groupids'], sys._getframe().f_code.co_name)

def hostgroup_get(name):
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

def hostgroup_delete(name):
    id = hostgroup_get(name)
    param = [ 
         id,]  
    all = zapi.do_request('hostgroup.delete', param)
    #print (all['result'])
    print ('delete hostgroup={},{}'.format(id, sys._getframe().f_code.co_name))


def template_create(name, hostgroup_name):
    gid = hostgroup_get(hostgroup_name) 
    param = {
        "host": name,
        "groups": { 
          "groupid": gid 
        }
    }
 
    all = zapi.do_request('template.create', param)
    print (all['result']['templateids'], sys._getframe().f_code.co_name)

def template_get(name):
    param = {
        "output": "extend",
        "filter": { 
          "host": [name] 
        }
    }
    all = zapi.do_request('template.get', param)
    #print (all['result'])
    tid = all['result'][0]['templateid']
    print("tid={}".format(tid), sys._getframe().f_code.co_name)
    return (tid)

def template_delete(name):
    id = template_get(name)
    param = [ 
         id,]  
    all = zapi.do_request('template.delete', param)
    print (all['result']['templateids'], sys._getframe().f_code.co_name)


def host_create(host_name, host_ip, host_port, hostgroup_name, template_name):
    gid = hostgroup_get(hostgroup_name) 
    tid = template_get(template_name)
    param = {
        "host": host_name,
        "name": host_name,
        "interfaces": [
            {
                "type": 1,#agent
                "main": 1,
                "useip": 1,
                "ip": host_ip,
                "dns": "",
                "port": host_port
            }
        ],
        "groups": [
            {
                "groupid": gid
            }
        ],
        "templates": [
            {
                "templateid": tid
            }
        ],


    }
    all = zapi.do_request('host.create', param)
    print (all['result']['hostids'], sys._getframe().f_code.co_name)


def host_get(name):
    param = {
        "output": "extend",
        "filter": {"host": name},

    }
    all = zapi.do_request('host.get', param)
    #print (all['result'])
    hostid = all['result'][0]['hostid']
    print("hostid={}".format(hostid), sys._getframe().f_code.co_name)
    return (hostid)

def host_delete(name):
    id = host_get(name)
    param = [ 
         id,]  
    all = zapi.do_request('host.delete', param)
    print (all['result']['hostids'], sys._getframe().f_code.co_name)

#oracle.query[zabbix,zabbix,cfBareos,XE,redowrites]
#oracle.query[zabbix,zabbix,cfBareos,XE,tablespace,SYSTEM]
def item_create(name, key, template_name):
    tid = template_get(template_name)
    param = {
        "name": name,
        "key_": key,
        "hostid": tid, #(real template id)--ID of the host or template that the item belongs to.
        "type": 0, #agent
        "value_type": 3, # unsigned numeric
        "interfaceid": "",
        "delay": "60s",
    }
 
    all = zapi.do_request('item.create', param)
    print (all['result']['itemids'], sys._getframe().f_code.co_name)

def item_get(key):
    #tid = template_get(template_name)
    param = {
        "output": "extend",
        #"hostids": tid,
        #"filter": {"hostid": hostid},
        #"filter": {"hostids": hid},
        "search": {"key_": key},
        "sortfield": "name",
    }
    all = zapi.do_request('item.get', param)
    items = []
    for i in all['result']:
        items.append(i['itemid'])
    #print (all['result'])
    print("1itemsssssssss", items, sys._getframe().f_code.co_name)
    return (items)


# monitor item also latest values based on host, like history
def item_get_by_host(host_name):
    hostid = host_get(host_name)
    param = {
        "output": ['hostid', 'itemid', 'status', 'lastclock','lastvalue','name'],
        "filter": {"hostid": hostid, 'status':'0'}
    }
    all = zapi.do_request('item.get', param)
    #print (all['result'])
    itemid = all['result'][0]['itemid']
    print("itemid={}".format(itemid), sys._getframe().f_code.co_name)
    return (itemid)


def item_delete(key):
    itemids = item_get(key)
    param = [itemids[0]] # first item id which is related with template, not host, can be delete
    print ('to delete item', itemids, param)
    all = zapi.do_request('item.delete', param)
    print (all['result']['itemids'], sys._getframe().f_code.co_name)



# data_type, value_type: 0 numeric float,1-character,2-log,3-numeric unsigned,4-text 
def history_get(key):
    itemids = item_get(key)
    print ("itemids", itemids)
    param = {
        "output": "extend",
        "history": 3,
        "itemids": itemids,
        "sortfield": "clock",
        "sortorder": "DESC",
        "limit": 30
    }
    all = zapi.do_request('history.get', param)
    print (all['result'], sys._getframe().f_code.co_name)

'''

{CF_Template713:oracle.query[zabbix,zabbix,cfBareos,XE,tablespace,SYSTEM].last()}>0
{CF_Host713:oracle.query[zabbix,zabbix,cfBareos,XE,tablespace,SYSTEM].last()}>0
{CF_Host713:oracle.query[zabbix,zabbix,cfBareos,XE,tablespace,SYSTEM].last()}>10
expr = "{"+"{0}:xxxxxxxxxxxxx.last()".format(host)+"}"+">10" 
'''
def trigger_create_lastfun(desc, host, key):
    expr = "{"+"{0}:{1}.last()".format(host,key)+"}"+">10" 
    print ("EEEXXXexpr=", expr)
    param = {
        "description": desc,
        "expression": expr
    }
  
    all = zapi.do_request('trigger.create', param)
    print (all['result']['triggerids'], sys._getframe().f_code.co_name)

# trigger get by host (restart zabbix-agent or wait more time???)
def trigger_get_by_host(host_name):
    hostid = host_get(host_name)
    param = {
        "output": ["triggerid", "description","priority"],
        "selectHosts":"",
        "filter": {"hostid":hostid,"status":"0","value":"1"}, #value 1: problem.?.
        "sortfield": "priority",
        "sortorder": "DESC"
    }
 
    all = zapi.do_request('trigger.get', param)
    print ('trigger result:',all['result'])
    # [{u'priority': u'0', u'triggerid': u'15641', u'hosts': [{u'hostid': u'10260'}], u'description': u'tablespace>10 trigger'}]
    tid = all['result'][0]['triggerid']
    print('tid==============triggerid', tid, sys._getframe().f_code.co_name)
    return (tid)


def trigger_delete(host_name):
    triggerid = trigger_get_by_host(host_name)
    print ('try delete', triggerid)
    param = [triggerid]
    all = zapi.do_request('trigger.delete', param)
    print (all['result']['triggerids'], sys._getframe().f_code.co_name)


def host_getxx(zapi):
    """获取所有主机及其监控状态"""
    print ('auth:', zapi.auth)

    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "auth": zapi.auth,
        "method": "host.get",

        "params": {
            "output": [
                "host",
                "available",
            ],
        },


    }
    res = zapi.call_json_api(data)
    if res.get("result"):
        #以字典格式返回主机IP和对应监控状态：0为unknown、1为正常、2为异常
        print ('res:', res)
        hosts = [(h["host"], h["available"]) for h in res["result"]]
        print ('hosts1:', hosts)
        return hosts
    else:
        faild("Error: %s" % res["error"]["data"])

if __name__ == '__main__xx':
    zapi = ZabbixAPI("http://118.31.109.239/zabbix")
    zapi.login("Admin", "zabbix")
    print ("Connected ZAPI version %s" % zapi.api_version())


    #hostgroup_create('CF_Group713')
    gid = hostgroup_get('CF_Group713')
    print (gid, type(gid))
    #hostgroup_delete('CF_Group713')

    #template_create('CF_Template713', 'CF_Group713')
    tid = template_get('CF_Template713')
    #template_delete('CF_Template713')
    print ("tttemplate!!!=id=", tid)

    key = "oracle.query[zabbix,zabbix,cfBareos,XE,tablespace,SYSTEM]"
    #item_create("CF_Item_tbl_system", key, "CF_Template713")
    iid = item_get(key)
    print ("item....:", iid)
    #item_delete(key)

    #host_create("CF_Host713", "172.16.111.55","10050", "CF_Group713", "CF_Template713")
    hostid = host_get("CF_Host713")
    print ("hostid={}".format(hostid))
    item_get_by_host("CF_Host713")
    print ("host item get after host created=======")
    #host_delete('CF_Host713')
 

    """ 
    [{u'itemid': u'28272', u'status': u'0', u'lastvalue': u'60', u'hostid': u'10260', u'name': u'CF_Item_tbl_system', u'lastclock': u'1563031694'}]
    itemid=28272
    """
    print("-----history----")
    ##history_get(key)
    history_get(key)

    desc="tablespace>10 trigger"
    host="CF_Host713"
    key="oracle.query[zabbix,zabbix,cfBareos,XE,tablespace,SYSTEM]"
    #trigger_create_lastfun(desc, host, key)
    print ('0-----get trigger-----')
    ##trigger_get_by_host(host)
    trigger_get_by_host(host)
    print ('1-----get trigger-----')
    #trigger_delete(host) 

   
'''
    host_getxx(zapi)

    h2 = [(h["host"], h["available"]) for h in zapi.host.get(output=["host", "available"])]
    print ("hosts2:", h2)

    h22 = [(h["host"], h["available"]) for h in zapi.host.get(filter={'available': 1}, output=["host", "available"])]
    print ("hosts2:", h22)

    resultNoFilter = zapi.do_request('host.get', {'available': 0, 'output':["host", "available"]})
    print ("hostsNoFileter no condition:", resultNoFilter)


    result3 = zapi.do_request('host.get', {'filter': {'available': 0}, 'output':["host", "available"]})
    print ("hosts3:", result3['result'])

    result4 = zapi.do_request('host.get', {'filter': {'available': 1}, "output":["host", "available"]})
    print ("hosts4:", result4['result'])
   
# Zabbix server - cf_trigger_t1 (Unack)
triggers = zapi.trigger.get(only_true=1,
                            skipDependent=1,
                            monitored=1,
                            active=1,
                            output='extend',
                            expandDescription=1,
                            selectHosts=['host'],
                            )
print (triggers)
# Do another query to find out which issues are Unacknowledged
unack_triggers = zapi.trigger.get(only_true=1,
                                  skipDependent=1,
                                  monitored=1,
                                  active=1,
                                  output='extend',
                                  expandDescription=1,
                                  selectHosts=['host'],
                                  withLastEventUnacknowledged=1,
                                  )
print (unack_triggers)
unack_trigger_ids = [t['triggerid'] for t in unack_triggers]
for t in triggers:
    t['unacknowledged'] = True if t['triggerid'] in unack_trigger_ids \
        else False

# Print a list containing only "tripped" triggers
for t in triggers:
    if int(t['value']) == 1:
        print("{0} - {1} {2}".format(t['hosts'][0]['host'],
                                     t['description'],
                                     '(Unack)' if t['unacknowledged'] else '')
              ) 
'''
