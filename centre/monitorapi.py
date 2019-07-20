#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from centre.zabbixlib import ZabbixAPI
from centre.zabbixlib import logger
from centre.configs import *
#from centre.hostgroup import *
#import *.....

#loging, class module, testing, items for monitors, exception handling, and use json param py
# method/params

zapi = ZabbixAPI(Zserver)
zapi.login(Zusername, Zpassword)
logger.info("Connected ZAPI version %s" % zapi.api_version())


#To improve the logging when url not connecting!!!
#Class MonitorAPI:
class MonitorAPI:
    def __init__(self, zapi):
        self.__zapi = zapi
    
    #single functions

    #hostgroup
    '''
    [{u'internal': u'0', u'flags': u'0', u'groupid': u'16', u'name': u'CF DB Srv1'}
    '''
    def hostgroup_create(self, name):
        param = {
            "name": name 
        }
        resp = self.__zapi.do_request('hostgroup.create', param)
        if not resp or not resp['result']:
            return None
        return (resp['result']['groupids'])
    
    def hostgroup_get(self, name):
        param = {
            "filter": { 
              "name": [name,]
            }
        }
        resp = self.__zapi.do_request('hostgroup.get', param)
        if not resp or not resp['result']:
            return (None)
        groupid = resp['result'][0]['groupid']
        return (groupid)
    
    def hostgroup_delete(self, name):
        id = self.hostgroup_get(name)
        param = [ 
             id,]  
        resp = self.__zapi.do_request('hostgroup.delete', param)
        if not resp or not resp['result']:
            return None
        return (resp['result']['groupids'])

    #template
    def template_create(self, name, hostgroup_name):
        gid = self.hostgroup_get(hostgroup_name) 
        param = {
            "host": name,
            "groups": { 
              "groupid": gid 
            }
        }
     
        resp = self.__zapi.do_request('template.create', param)
        if not resp or not resp['result']:
            return None
        return (resp['result']['templateids'])
    
    def template_get(self, name):
        param = {
            "output": "extend",
            "filter": { 
              "host": [name] 
            }
        }
        resp = self.__zapi.do_request('template.get', param)
        if not resp or not resp['result']:
            return None
        tid = resp['result'][0]['templateid']
        return (tid)
    
    def template_delete(self, name):
        id = self.template_get(name)
        param = [ 
             id,]  
        resp = self.__zapi.do_request('template.delete', param)
        if not resp or not resp['result']:
            return None
        tid = resp['result']['templateids']
        return (tid) 

    #item  value_type 
    #oracle.query[zabbix,zabbix,cfBareos,XE,redowrites]
    #oracle.query[zabbix,zabbix,cfBareos,XE,tablespace,SYSTEM]
    def item_create(self, name, key, template_name):
        tid = self.template_get(template_name)
        param = {
            "name": name,
            "key_": key,
            "hostid": tid, #(real template id)--ID of the host or template that the item belongs to.
            "type": 0, #agent
            "value_type": 3, # unsigned numeric
            "interfaceid": "",
            "delay": "60s",
        }
     
        resp = self.__zapi.do_request('item.create', param)
        if not resp or not resp['result']:
            return None
        itemids = resp['result']['itemids']
        return (itemids)
    
    def item_get(self, key):
        param = {
            "output": "extend",
            #"hostids": tid,
            #"filter": {"hostid": hostid},
            #"filter": {"hostids": hid},
            "search": {"key_": key},
            "sortfield": "name",
        }
        resp = self.__zapi.do_request('item.get', param)
        if not resp or not resp['result']:
            return None
        items = []
        for i in resp['result']:
            items.append(i['itemid'])
        logger.debug("items:{} in {}".format(items, sys._getframe().f_code.co_name))
        return (items)
 
    def item_delete(self, key):
        itemids = self.item_get(key)
        param = [itemids[0]] # first item id which is related with template, not host, can be delete
        resp = self.__zapi.do_request('item.delete', param)
        if not resp or not resp['result']:
            return None
        return (resp['result']['itemids'])
    
 
    '''
    {CF_Template713:oracle.query[zabbix,zabbix,cfBareos,XE,tablespace,SYSTEM].last()}>0
    {CF_Host713:oracle.query[zabbix,zabbix,cfBareos,XE,tablespace,SYSTEM].last()}>0
    {CF_Host713:oracle.query[zabbix,zabbix,cfBareos,XE,tablespace,SYSTEM].last()}>10
    expr = "{"+"{0}:xxxxxxxxxxxxx.last()".format(host)+"}"+">10" 
    '''
    def trigger_create(self, desc, host, key, func, compareto):
        #expr = "{"+"{0}:{1}.last()".format(host,key)+"}"+">10" 
        expr = "{"+"{0}:{1}.{2}".format(host,key,func)+"}" + compareto 
        print ("EEEXXXexpr=", expr)
        param = {
            "description": desc,
            "expression": expr
        }
      
        resp = self.__zapi.do_request('trigger.create', param)
        if not resp or not resp['result']:
            return None
        tiggerids = resp['result']['triggerids']
        return tiggerids 

    # trigger get by host (restart zabbix-agent or wait more time???)
    def trigger_get_by_host(self, host_name):
        hostid = self.host_get(host_name)
        param = {
            "output": ["triggerid", "description","priority"],
            "selectHosts":"",
            "filter": {"hostid":hostid,"status":"0","value":"1"}, #value 1: problem.?.
            "sortfield": "priority",
            "sortorder": "DESC"
        }
     
        resp = self.__zapi.do_request('trigger.get', param)
        if not resp or not resp['result']:
            return None
          
        triggerid = resp['result'][0]['triggerid']
        return triggerid
        # [{u'priority': u'0', u'triggerid': u'15641', u'hosts': [{u'hostid': u'10260'}], u'description': u'tablespace>10 trigger'}]
    
    
    def trigger_delete(self, host_name):
        triggerid = self.trigger_get_by_host(host_name)
        param = [triggerid]
        resp = self.__zapi.do_request('trigger.delete', param)
        if not resp or not resp['result']:
            return None
        triggerid = resp['result']['triggerids']
        return triggerids
    

    def host_create(self, host_name, host_ip, host_port, hostgroup_name, template_name):
        gid = self.hostgroup_get(hostgroup_name) 
        tid = self.template_get(template_name)
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
        resp = self.__zapi.do_request('host.create', param)
        if not resp or not resp['result']:
            return None
        hostids = resp['result']['hostids']
        return hostids 
    
    def host_get(self, name):
        param = {
            "output": "extend",
            "filter": {"host": name},
    
        }
        resp = self.__zapi.do_request('host.get', param)
        if not resp or not resp['result']:
            return None
        hostid = resp['result'][0]['hostid']
        return (hostid)
    
    def host_delete(self, name):
        id = self.host_get(name)
        param = [ 
             id,]  
        resp = self.__zapi.do_request('host.delete', param)
        if not resp or not resp['result']:
            return None
        
        hostids = resp['result']['hostids']
        return hostids

    # monitor item also latest values based on host, like history
    def item_get_by_host(self, host_name):
        hostid = self.host_get(host_name)
        param = {
            "output": ['hostid', 'itemid', 'status', 'lastclock','lastvalue','name'],
            "filter": {"hostid": hostid, 'status':'0'}
        }
        resp = self.__zapi.do_request('item.get', param)
        if not resp or not resp['result']:
            return None
        #itemid = resp['result'][0]['itemid']
        return resp['result']
    
    # data_type, value_type: 0 numeric float,1-character,2-log,3-numeric unsigned,4-text 
    def history_get(self, key):
        itemids = self.item_get(key)
        print ("itemids", itemids)
        param = {
            "output": "extend",
            "history": 3,
            "itemids": itemids,
            "sortfield": "clock",
            "sortorder": "DESC",
            "limit": 30
        }
        resp = self.__zapi.do_request('history.get', param)
        if not resp or not resp['result']:
            return None
        return resp['result']


    def host_get_abnormal(self):
        """获取所有主机及其监控状态"""
        data = {
            "jsonrpc": "2.0",
            "id": 1,
            "auth": self.__zapi.auth,
            "method": "host.get",
    
            "params": {
                "output": [
                    "host",
                    "available",
                ],
            },
    
    
        }
        resp = self.__zapi.call_json_api(data)
        if not resp or not resp['result']:
            return None
 
        #以字典格式返回主机IP和对应监控状态：0为unknown、1为正常、2为异常
        hosts = [(h["host"], h["available"]) for h in res["result"]]
        return hosts
    
    def hostmacro_create(self, host_name, varmacro, value):
        hostid = self.host_get(host_name)
        param = {
            "hostid": hostid,
            "macro": varmacro,
            "value": value,
    
        }
        resp = self.__zapi.do_request('usermacro.create', param)
        if not resp or not resp['result']:
            return None
        ids = resp['result']['hostmacroids']
        return (ids)


    def hostmacro_get(self, host_name):
        hostid = self.host_get(host_name)
        param = {
            "output": "extend",
            "hostids": hostid
        }
        resp = self.__zapi.do_request('usermacro.get', param)
        if not resp or not resp['result']:
            return None
        macroids = []
        for i in resp['result']:
            macroids.append(i['hostmacroid'])
        return macroids

    def hostmacro_delete(self, host_name):
        ids = hostmacro_get(host_name)
        param = ids 
        resp = self.__zapi.do_request('usermacro.delete', param)
        if not resp or not resp['result']:
            return None
        ids = resp['result']['hostmacroids']
        return (ids)

        
    #combine function 
    def transaction_create_item_on_template(self, template_name):
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




        pass
    
    def template_import(self, path):
        rules = {
            'applications': {
                'createMissing': True,
            },
            'discoveryRules': {
                'createMissing': True,
                'updateExisting': True
            },
            'graphs': {
                'createMissing': True,
                'updateExisting': True
            },
            'groups': {
                'createMissing': True
            },
            'hosts': {
                'createMissing': True,
                'updateExisting': True
            },
            'images': {
                'createMissing': True,
                'updateExisting': True
            },
            'items': {
                'createMissing': True,
                'updateExisting': True
            },
            'maps': {
                'createMissing': True,
                'updateExisting': True
            },
            'screens': {
                'createMissing': True,
                'updateExisting': True
            },
            'templateLinkage': {
                'createMissing': True,
            },
            'templates': {
                'createMissing': True,
                'updateExisting': True
            },
            'templateScreens': {
                'createMissing': True,
                'updateExisting': True
            },
            'triggers': {
                'createMissing': True,
                'updateExisting': True
            },
            'valueMaps': {
                'createMissing': True,
                'updateExisting': True
            },
        }
        
        if os.path.isdir(path):
            files = glob.glob(path+'/*.xml')
            for file in files:
                print(file)
                with open(file, 'r') as f:
                    template = f.read()
                    try:
                        result = self.__zapi.confimport('xml', template, rules)
                        print (result)
                    except ZabbixAPIException as e:
                        print(e)
                print('')
        elif os.path.isfile(path):
            files = glob.glob(path)
            for file in files:
                with open(file, 'r') as f:
                    template = f.read()
                    try:
                        result = self.__zapi.confimport('xml', template, rules)
                        print (result)
                    except ZabbixAPIException as e:
                        print(e)
        else:
            print('I need a xml file')

  
#create global instance for API usage
monitorAPI = MonitorAPI(zapi)

