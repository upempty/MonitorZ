#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
import glob
from centre.zabbixlib import ZabbixAPI, ZabbixAPIException
from centre.zabbixlib import logger
from centre.configs import *
import time
#from centre.hostgroup import *
#import *.....

#loging, class module, testing, items for monitors, exception handling, and use json param py
# method/params

#zapi = ZabbixAPI(Zserver)
'''
try: 
    zapi.login(Zusername, Zpassword)
except ZabbixAPIException as e:
    print('try as zabbix', e)
    raise ZabbixAPIException("Received empty responsixxxxxxxxxxxxxxe")
logger.info("Connected ZAPI version %s" % zapi.api_version())
'''


#To improve the logging when url not connecting!!!
#Class MonitorAPI:
class MonitorAPI:
    #def __init__(self, zapi):
    def __init__(self):
        #self.__zapi = zapi
        self.__zapi = ZabbixAPI(Zserver)

    def tryme(func):
        def wrapper(*args):
            try:
                return func(*args)
            except Exception as e:
                logger.info("Try with Exception")
                logger.info(e)
                return None 
        return wrapper
        
    #single functions
    #hostgroup
    '''
    [{u'internal': u'0', u'flags': u'0', u'groupid': u'16', u'name': u'CF DB Srv1'}
    '''
    @tryme 
    def hostgroup_create(self, name):
        param = {
            "name": name 
        }
        resp = self.__zapi.do_request('hostgroup.create', param)
        if not resp or not resp['result']:
            return None
        return (resp['result']['groupids'][0])
    
    @tryme 
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
    
    @tryme 
    def hostgroup_delete(self, name):
        id = self.hostgroup_get(name)
        param = [ 
             id,]  
        resp = self.__zapi.do_request('hostgroup.delete', param)
        if not resp or not resp['result']:
            return None
        return (resp['result']['groupids'])

    #template
    @tryme 
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
        return (resp['result']['templateids'][0])
    
    @tryme 
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
    
    @tryme 
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
    @tryme 
    def item_create(self, name, key, value_type, template_name):
        tid = self.template_get(template_name)
        param = {
            "name": name,
            "key_": key,
            "hostid": tid, #(real template id)--ID of the host or template that the item belongs to.
            "type": 0, #agent
            "value_type": value_type, # 3 unsigned numeric
            "interfaceid": "",
            #"delay": "60s", not supported by 3.2.11, but 3.4.15
            "delay": "60",
        }
        resp = self.__zapi.do_request('item.create', param)
        if not resp or not resp['result']:
            return None
        itemids = resp['result']['itemids']
        logger.info("create items {}".format(itemids))
        return (itemids[0])
    
    @tryme 
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
 
    @tryme 
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
    @tryme 
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
        return tiggerids[0] 

    @tryme 
    def trigger_get(self, host_name, desc):
        hostid = self.host_get(host_name)
        param = {
            "output": ["triggerid", "description","priority"],
            "selectHosts":"",
            "filter": {"hostid":hostid},
            "sortfield": "priority",
            "sortorder": "DESC"
        }
        resp = self.__zapi.do_request('trigger.get', param)
        if not resp or not resp['result']:
            return None
        for i in resp['result']:
            if i['description'] == desc:
                print ('already exists: {}'.format(i))
                return i['triggerid']
        return None
 

    @tryme 
    def trigger_get_problem_by_desc(self, host_name, desc):
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
        for i in resp['result']:
            if i['description'] == desc:
                print ('problem {}'.format(i))
                return i['triggerid']
        return None
 
    # trigger get by host (restart zabbix-agent or wait more time???)
    @tryme 
    def trigger_get_problem_by_host(self, host_name):
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
        triggerids = []
        for i in resp['result']:
            triggerids.append(i['triggerid'])
            print ('host problem {}'.format(i))
         
        return triggerids
        # [{u'priority': u'0', u'triggerid': u'15641', u'hosts': [{u'hostid': u'10260'}], u'description': u'tablespace>10 trigger'}]
    
    
    @tryme 
    def trigger_delete(self, host_name, desc):
        triggerid = self.trigger_get(host_name, desc)
        param = [triggerid]
        resp = self.__zapi.do_request('trigger.delete', param)
        if not resp or not resp['result']:
            return None
        triggerid = resp['result']['triggerids']
        return triggerids
    

    @tryme 
    def host_create(self, host_name, host_ip, host_port, hostgroup_name, template_name):
        gid = self.hostgroup_get(hostgroup_name) 
        if not gid:
           return None
        tid = self.template_get(template_name)
        if not tid:
           return None
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
        return hostids[0] 

    @tryme 
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
    
    @tryme 
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
    @tryme 
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
    @tryme 
    def history_get(self, key, value_type):
        itemids = self.item_get(key)
        #print ("itemids", itemids)
        param = {
            "output": "extend",
            "history": value_type,
            "itemids": itemids,
            "sortfield": "clock",
            "sortorder": "DESC",
            "limit": 10
        }
        resp = self.__zapi.do_request('history.get', param)
        if not resp or not resp['result']:
            return None

        logger.info('========================================')
        logger.info('item:{} history raw result=='.format(key))
        for i,j in enumerate(resp['result']):
            logger.info('{}: {}'.format(i, j))

        logger.info('\nitem:{} history human format result=='.format(key))
        for i,j in enumerate(resp['result']):
            timestr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(long(j['clock'])))
            logger.info('item:{}, id:{}, value:{}, time:{}'.format(key, j['itemid'],j['value'], timestr))

        return resp['result']


    @tryme 
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
        hosts = [(h["host"], h["available"]) for h in resp["result"]]
        logger.debug('hosts: {}'.format(hosts))
        return hosts
    
    @tryme 
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
        return (ids[0])


    @tryme 
    def hostmacro_get(self, host_name, varmacro):
        hostid = self.host_get(host_name)
        param = {
            "output": "extend",
            "hostids": hostid
        }
        resp = self.__zapi.do_request('usermacro.get', param)
        if not resp or not resp['result']:
            return None
        for i in resp['result']:
            if i['macro'] == varmacro:
                return i['hostmacroid']
        return None

    @tryme 
    def hostmacro_delete(self, host_name, varmacro):
        id = hostmacro_get(host_name, varmacro)
        param = [id] 
        resp = self.__zapi.do_request('usermacro.delete', param)
        if not resp or not resp['result']:
            return None
        ids = resp['result']['hostmacroids']
        return (ids)

        
    #combine function 
    @tryme 
    def transaction_create_item_on_template(self, hostgroup_name,template_name, item_name, key, value_type):
        gid = self.hostgroup_get(hostgroup_name)
        if not gid:
            gid = self.hostgroup_create(hostgroup_name)
        tid = self.template_get(template_name)
        if not tid:
            tid = self.template_create(template_name, hostgroup_name)
        #key = "oracle.query[zabbix,zabbix,cfBareos,XE,tablespace,SYSTEM]"
        #item_create("CF_Item_tbl_system", key, "CF_Template713")
        ids = self.item_get(key)
        if not ids:
            ids = self.item_create(item_name, key, value_type, template_name)
        return ids[0] 

    @tryme 
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
                    except ZabbixAPIException as e:
                        print(e)
                print('')
        elif os.path.isfile(path):
            files = glob.glob(path)
            for file in files:
                print(file)
                with open(file, 'r') as f:
                    template = f.read()
                    try:
                        result = self.__zapi.confimport('xml', template, rules)
                    except ZabbixAPIException as e:
                        print(e)
        else:
            print('I need a xml file')

  
#create global instance for API usage
#monitorAPI = MonitorAPI(zapi)

