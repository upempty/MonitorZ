#!/usr/bin/env python
#-*- coding: utf-8 -*-

from centre.monitorapi import *


if __name__ == '__main__':

    monitorAPI.hostgroup_get('CF_Group713')
    monitorAPI.hostgroup_get('CF_Group713xxxxx')
    #logger.info('a=== {}'.format(a))
    #monitorAPI.host_get('CF_Host713')
    


    #hostgroup_create('CF_Group713')
    #gid = hostgroup_get('CF_Group713')
 

if __name__ == '__main__xx':
    #zapi = ZabbixAPI("http://118.31.109.239/zabbix")
    #zapi.login("Admin", "zabbix")
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



