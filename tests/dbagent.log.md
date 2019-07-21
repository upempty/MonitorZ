## testing logging
```
('dir selfs name one by one', 'show_tablespaces_temp', [])
('dir selfs name one by one', 'show_users', [])
('dir selfs name one by one', 'tablespace', ['name'])
('dir selfs name one by one', 'tablespace_abs', ['name'])
('dir selfs name one by one', 'tablespace_temp', ['name'])
('dir selfs name one by one', 'tblrowsscans', [])
('dir selfs name one by one', 'tblscans', [])
('dir selfs name one by one', 'uptime', [])
('dir selfs name one by one', 'user_status', ['dbuser'])
('dir selfs name one by one', 'version', [])
('self.args', Namespace(address='127.0.0.1', argnames=['name'], database='XE', func=<bound method Main.tablespace of <__main__.Main object at 0x7f4cbabaa950>>, name='SYSTEM', password='zabbix', port=None, username='zabbix'))
60
[root@cfBareos agent]# python dbagent.py --username zabbix --password zabbix --address 127.0.0.1 --database XE tablespace SYSTEM

=====
python agent/dbagent.py --username zabbix --password zabbix --address 127.0.0.1 --database XE dbsize
python agent/dbagent.py --username zabbix --password zabbix --address cfBareos --database XE dbsize

zabbix_get -s cfBareos -p 10050 -k oracle.query[zabbix,zabbix,cfBareos,XE,dbfilesize]
zabbix_get -s cfBareos -p 10050 -k oracle.query[zabbix,zabbix,cfBareos,XE,dbsize]
zabbix_get -s cfBareos -p 10050 -k oracle.query[zabbix,zabbix,cfBareos,XE,version]
zabbix_get -s cfBareos -p 10050 -k oracle.query[zabbix,zabbix,cfBareos,XE,check_active]


"{$USERNAME}"="zabbix"
"{$PASSWORD}"="zabbix"
"{$ADDRESS}"="cfBareos"
"{$DATABASE}"="XE"

{template721:oracle.query[zabbix,zabbix,cfBareos,XE,version].strlen()}>0


sqlplus /nolog
conn / as sysdba
SQL> conn / as sysdba

oracle.query[{$USERNAME},{$PASSWORD},{$ADDRESS},{$DATABASE},check_active]

pyora[{$USERNAME},{$PASSWORD},{$ADDRESS},{$DATABASE},check_archive,{$ARCHIVE}]




```
