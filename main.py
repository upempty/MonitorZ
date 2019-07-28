#!/usr/bin/env python
#-*- coding: utf-8 -*-

from centre.monitorapi import *


if __name__ == '__main__':
    '''

    oracle.query[zabbix,zabbix,cfBareos,XE,tablespace,SYSTEM]
    '''
    monitorAPI = MonitorAPI()
    ''' 
    host_name = "host721" 
    hid = monitorAPI.host_get(host_name)
    print (hid)
    exit(0) 
    '''

    hostgroup_name = 'hostgroup721'
    template_name = 'template721'
    item_name = 'ora version'
    key = 'oracle.query[zabbix,zabbix,cfBareos,XE,version]'
    value_type = 1
    item_name2 = 'ora db size'
    key2 = 'oracle.query[zabbix,zabbix,cfBareos,XE,dbsize]'
    value_type2 = 3 
    item_name3 = 'ora check active'
    key3 = 'oracle.query[{$USERNAME},{$PASSWORD},{$ADDRESS},{$DATABASE},check_active]'
    value_type3 = 3 


    monitorAPI.transaction_create_item_on_template(hostgroup_name,
                                                   template_name, 
                                                   item_name, 
                                                   key, 
                                                   value_type)

    monitorAPI.transaction_create_item_on_template(hostgroup_name,
                                                   template_name, 
                                                   item_name2, 
                                                   key2, 
                                                   value_type2)

    monitorAPI.transaction_create_item_on_template(hostgroup_name,
                                                   template_name, 
                                                   item_name3, 
                                                   key3, 
                                                   value_type3)

    host_name = "host721" 
    ip = "172.16.111.55"
    port = "10050"
    hid = monitorAPI.host_get(host_name)
    if not hid:
        monitorAPI.host_create(host_name, ip, port, hostgroup_name, template_name)
    
    '''
    "{$USERNAME}"="zabbix"
    "{$PASSWORD}"="zabbix"
    "{$ADDRESS}"="cfBareos"
    "{$DATABASE}"="XE"
    '''
    macro1 = "{$USERNAME}"
    value1 = "zabbix"
    macro2 = "{$PASSWORD}"
    value2 = "zabbix"
    macro3 = "{$ADDRESS}"
    value3 = "cfBareos"
    macro4 = "{$DATABASE}"
    value4 = "XE"

    id = monitorAPI.hostmacro_get(host_name, macro1)
    if not id:
        monitorAPI.hostmacro_create(host_name, macro1, value1)
    id2 = monitorAPI.hostmacro_get(host_name, macro2)
    if not id2:
        monitorAPI.hostmacro_create(host_name, macro2, value2)
    id3 = monitorAPI.hostmacro_get(host_name, macro3)
    if not id3:
        monitorAPI.hostmacro_create(host_name, macro3, value3)
    id4 = monitorAPI.hostmacro_get(host_name, macro4)
    if not id4:
        monitorAPI.hostmacro_create(host_name, macro4, value4)
    
    monitorAPI.history_get(key, value_type)
    monitorAPI.history_get(key3, value_type3)
    monitorAPI.host_get_abnormal()

    desc3 = "It is fake active" 
    func3 = "last()" 
    compareto3 = ">0"
    triggerid = monitorAPI.trigger_get(host_name, desc3)
    if not triggerid:
        triggerid = monitorAPI.trigger_create(desc3, host_name, key3, func3, compareto3)
    monitorAPI.trigger_get_problem_by_desc(host_name, desc3)
    monitorAPI.trigger_get_problem_by_host(host_name)
   


 

    #OracleTemplateHostGroup721 needs to be created as first condition
    hostgroup_namebatch = "OracleTemplateHostGroup721" 
    gid = monitorAPI.hostgroup_get(hostgroup_namebatch)
    if not gid:
       gid = monitorAPI.hostgroup_create(hostgroup_namebatch)
    path = './centre/xml' 
    monitorAPI.template_import(path)

if __name__ == '__main__xx':
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



