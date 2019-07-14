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

```
