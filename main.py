#!/usr/bin/env python
#-*- coding: utf-8 -*-

from centre.monitorapi import *

'''
zabbix_server (Zabbix) 3.2.11
zabbix_agentd (daemon) (Zabbix) 3.2.1
# data_type, value_type: 0 numeric float,1-character,2-log,3-numeric unsigned,4-text
'''


def test_create_templateitem_to_2host():

    # create template item
    hostgroup_name = 'HostgroupT1'
    template_name = 'TemplateT1'
    item_name = "NetsentT1"
    key = "oracle.query[{$USERNAME},{$PASSWORD},{$ADDRESS},{$DATABASE},netsent]"
    value_type = 3
    monitorAPI.transaction_create_item_on_template(hostgroup_name,
                                                  template_name, 
                                                  item_name, 
                                                  key, 
                                                  value_type)
    
    # create host with template
    host_name1 = "hostDB1T1"
    host_name2 = "hostDB2T1"
    host_ip1 = "192.168.1.7"
    host_ip2 = "192.168.1.8"
    port = "10050"
    hid = monitorAPI.host_get(host_name1)
    if not hid:
        monitorAPI.host_create(host_name1, host_ip1, port, hostgroup_name, template_name)
    hid = monitorAPI.host_get(host_name2)
    if not hid:
        monitorAPI.host_create(host_name2, host_ip2, port, hostgroup_name, template_name)

    '''
    # create macro based on host
    zmacros = [{"hostname":"hostDB1", "macro":"{$USERNAME}", "value":"zabbix"}, 
               {"hostname":"hostDB1", "macro":"{$PASSWORD}", "value":"zabbix"}, 
               {"hostname":"hostDB1", "macro":"{$ADDRESS}", "value":"192.168.1.7"}, 
               {"hostname":"hostDB1", "macro":"{$DATABASE}", "value":"orcl"}, 
			   
               {"hostname":"hostDB2", "macro":"{$USERNAME}", "value":"zabbix"}, 
               {"hostname":"hostDB2", "macro":"{$PASSWORD}", "value":"zabbix"}, 
               {"hostname":"hostDB2", "macro":"{$ADDRESS}", "value":"192.168.1.8"}, 
               {"hostname":"hostDB2", "macro":"{$DATABASE}", "value":"orcl"}
              ]
    '''


    # create macro based on host
    zmacros = [{"hostname":host_name1, "macro":"{$USERNAME}", "value":"zabbix"}, 
               {"hostname":host_name1, "macro":"{$PASSWORD}", "value":"zabbix"}, 
               {"hostname":host_name1, "macro":"{$ADDRESS}", "value":"192.168.1.7"}, 
               {"hostname":host_name1, "macro":"{$DATABASE}", "value":"orcl"}, 
			   
               {"hostname":host_name2, "macro":"{$USERNAME}", "value":"zabbix"}, 
               {"hostname":host_name2, "macro":"{$PASSWORD}", "value":"zabbix"}, 
               {"hostname":host_name2, "macro":"{$ADDRESS}", "value":"192.168.1.8"}, 
               {"hostname":host_name2, "macro":"{$DATABASE}", "value":"orcl"}
              ]

    for m in zmacros:
        id = monitorAPI.hostmacro_get(m["hostname"], m["macro"])
        if not id:
            monitorAPI.hostmacro_create(m["hostname"], m["macro"], m["value"])

    # check data
    monitorAPI.history_get_host(host_name1, key, value_type)
    monitorAPI.history_get_host(host_name2, key, value_type)



if __name__ == '__main__':
    '''

    oracle.query[zabbix,zabbix,cfBareos,XE,tablespace,SYSTEM]
    '''
    monitorAPI = MonitorAPI()

    test_create_templateitem_to_2host()
    sys.exit() 

    ''' 
    host_name = "host721" 
    hid = monitorAPI.host_get(host_name)
    print (hid)
    exit(0) 
    '''
    titem_name = "version"
    tkey = "oracle.query[zabbix,zabbix,192.168.1.7,orcl,version]"
    #key       = 'oracle.query[zabbix,zabbix,{},{},{}]'.format(agent1,db1,item["params"])
    #               {"func":"linux_cpucpu", "params":"system.cpu.util[,user]","value_type":0},  
    tvalue_type = 1

    host_name = "host823" 
    hid = monitorAPI.host_get(host_name)
    logger.info('host:{}, id:{}'.format(host_name, hid))

    template_name = 'template823'
    tid = monitorAPI.template_get(template_name)
    logger.info('template:{}, id:{}'.format(template_name, tid))

    print (titem_name, tkey, tvalue_type)
    monitorAPI.history_get(tkey, tvalue_type)


    #!!!!!!!!!
    sys.exit() 




    agent1 = "192.168.1.7"
    db1 = "orcl"
    hostgroup_name = 'hostgroup823'
    template_name = 'template823'

    #key = 'oracle.query[zabbix,zabbix,{},{},{}]'.format(agent1,db1,'version')
    #key = 'oracle.query[zabbix,zabbix,cfBareos,XE,version]'

    # "oracle.query[zabbix,zabbix,192.168.1.7,orcl,version]"    
    input_items = [{"func":"version", "params":"version","value_type":1}, 
                   {"func":"dbname", "params":"dbname","value_type":1},
                   {"func":"dbsystime", "params":"dbsystime","value_type":1},
                   {"func":"logmode", "params":"logmode","value_type":1},  
                   {"func":"dbstatus", "params":"dbstatus","value_type":1},  
                   {"func":"currentscn", "params":"currentscn","value_type":3},  
                   {"func":"archthreadseq", "params":"archthreadseq","value_type":1},  
                   {"func":"flash_areausage", "params":"flash_areausage","value_type":0},  
                   {"func":"backup_status", "params":"backup_status","value_type":1},  
                   {"func":"log_transfermode", "params":"log_transfermode","value_type":1},  
                   {"func":"show_users", "params":"show_users","value_type":4},  
                   {"func":"user_status", "params":"user_status,SYSTEM","value_type":1},  
                   {"func":"tablespace", "params":"tablespace,SYSTEM","value_type":3},  
                   {"func":"query_sessions", "params":"query_sessions","value_type":3},  
                   {"func":"query_lock", "params":"query_lock","value_type":3},  
                   {"func":"deadlocks", "params":"deadlocks","value_type":3},  
                   {"func":"query_redologs", "params":"query_redologs","value_type":3},  
                   {"func":"query_rollbacks", "params":"query_rollbacks","value_type":3},  
                   {"func":"check_archive", "params":"check_archive,DATA","value_type":3},  
                   {"func":"logfilesync", "params":"logfilesync","value_type":3},  
                   {"func":"bufbusywaits", "params":"bufbusywaits","value_type":3},  
                   {"func":"lastarclog", "params":"lastarclog","value_type":3},  
                   {"func":"redowrites", "params":"redowrites","value_type":3},  
                   {"func":"rollbacks", "params":"rollbacks","value_type":3},  
                   {"func":"commits", "params":"commits","value_type":3},  
                   {"func":"dbfilesize", "params":"dbfilesize","value_type":3},  
                   {"func":"rcachehit", "params":"rcachehit","value_type":0},  
                   {"func":"dsksortratio", "params":"dsksortratio","value_type":0},  
                   {"func":"linux_cpucpu", "params":"system.cpu.util[,user]","value_type":0},  
                   {"func":"linux_memorymem", "params":"vm.memory.size[pused]","value_type":0},  
                  ]

    #input_items = [{"func":"linux_cpucpu", "params":"system.cpu.util[,user]","value_type":0}]  
    '''
    item_name = input_items[0]["func"]
    key       = 'oracle.query[zabbix,zabbix,{},{},{}]'.format(agent1,db1,input_items[0]["params"])
    value_type = input_items[0]["value_type"] 

    print (key)
    print (input_items[0]["func"], item_name, input_items[0]["value_type"])
    print (item_name, key, value_type, len(input_items))
    '''

    for item in input_items:
        item_name = item["func"]
        if item_name.startswith("linux_"):
            key       = item["params"]
        else: 
            key       = 'oracle.query[zabbix,zabbix,{},{},{}]'.format(agent1,db1,item["params"])
        value_type = item["value_type"] 

        monitorAPI.transaction_create_item_on_template(hostgroup_name,
                                                       template_name, 
                                                       item_name, 
                                                       key, 
                                                       value_type)

    host_name = "host823" 
    #ip = "172.16.111.55"
    ip = agent1
    port = "10050"
    hid = monitorAPI.host_get(host_name)
    if not hid:
        monitorAPI.host_create(host_name, ip, port, hostgroup_name, template_name)



    for item in input_items:
        item_name = item["func"]
        if item_name.startswith("linux_"):
            key       = item["params"]
        else: 
            key       = 'oracle.query[zabbix,zabbix,{},{},{}]'.format(agent1,db1,item["params"])
        value_type = item["value_type"] 
        print ('\n\n')
        print (item_name, key, value_type)
        monitorAPI.history_get(key, value_type)



    #!!!!!!!!!
    sys.exit() 


    ''' 
    macro1 = "{$USERNAME}"
    value1 = "zabbix"
    macro2 = "{$PASSWORD}"
    value2 = "zabbix"
    macro3 = "{$ADDRESS}"
    value3 = "192.168.1.7"
    macro4 = "{$DATABASE}"
    value4 = "orcl"

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
    print("Beggen")
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

    '''
 
    print("williamtest1")
    #OracleTemplateHostGroup721 needs to be created as first condition

    ''' 
    hostgroup_namebatch = "OracleTemplateHostGroup721" 
    gid = monitorAPI.hostgroup_get(hostgroup_namebatch)
    if not gid:
       gid = monitorAPI.hostgroup_create(hostgroup_namebatch)
    path = './centre/xml' 
    monitorAPI.template_import(path)
   
    '''

