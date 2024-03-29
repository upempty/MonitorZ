#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import logging
from logging.handlers import TimedRotatingFileHandler
from centre.configs import *
import requests
import json

logger = logging.getLogger('monitorZ')
#stream log
stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.INFO)
logger.addHandler(stream)

#file log
filehandle = TimedRotatingFileHandler(LOG_FILE,when='D',interval=1,backupCount=30)
datefmt = '%Y-%m-%d %H:%M:%S'
format_str = '%(asctime)s %(levelname)s %(message)s'
formatter = logging.Formatter(format_str, datefmt)
filehandle.setFormatter(formatter)
logger.addHandler(filehandle)

logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.INFO)


class ZabbixAPIException(Exception):
    """ generic zabbix api exception
    code list:
         -32602 - Invalid params (eg already exists)
         -32500 - no permissions
    """
    pass


class ZabbixAPI(object):

    auth = ''

    def __init__(self,
                 server='http://localhost/zabbix',
                 session=None,
                 use_authenticate=False,
                 timeout=None):
        """
        Parameters:
            server: Base URI for zabbix web interface (omitting /api_jsonrpc.php)
            session: optional pre-configured requests.Session instance
            use_authenticate: Use old (Zabbix 1.8) style authentication
            timeout: optional connect and read timeout in seconds, default: None (if you're using Requests >= 2.4 you can set it as tuple: "(connect, read)" which is used to set individual 
connect and read timeouts.)
        """

        if session:
            self.session = session
        else:
            self.session = requests.Session()

        # Default headers for all requests
        self.session.headers.update({
            'Content-Type': 'application/json-rpc',
            'User-Agent': 'python/pyzabbix',
            'Cache-Control': 'no-cache'
        })

        self.use_authenticate = use_authenticate
        #self.auth = ''
        self.id = 0

        self.timeout = timeout

        self.url = server + '/api_jsonrpc.php'
        logger.info("JSON-RPC Server Endpoint: %s", self.url)

    def login(self, user='', password=''):
        """Convenience method for calling user.authenticate and storing the resulting auth token
           for further commands.
           If use_authenticate is set, it uses the older (Zabbix 1.8) authentication command
           :param password: Password used to login into Zabbix
           :param user: Username used to login into Zabbix
        """

        # If we have an invalid auth token, we are not allowed to send a login
        # request. Clear it before trying.
        self.auth = ''
        if self.use_authenticate:
            self.auth = self.user.authenticate(user=user, password=password)
        else:
            self.auth = self.user.login(user=user, password=password)

    def confimport(self, confformat='', source='', rules=''):
        """Alias for configuration.import because it clashes with
           Python's import reserved keyword
           :param rules:
           :param source:
           :param confformat:
        """

        return self.do_request(
            method="configuration.import",
            params={"format": confformat, "source": source, "rules": rules}
        )['result']

    def api_version(self):
        return self.apiinfo.version()

    #api2 with full json data
    def call_json_api(self, json_data):
        headers = {'content-type': 'application/json'}
        res = requests.post(self.url, data=json.dumps(json_data), headers=headers)
        return res.json()

    def do_request(self, method, params=None):
        if method == 'apiinfo.version' or method == 'user.login':
            return self.call_once(method, params)
        else:
            if not self.auth:
                loginparams = {'user': Zusername, 'password': Zpassword}
                self.auth = self.call_once('user.login', loginparams)['result']
            return self.call_once(method, params)
    
    #api1 with seperate method + params: dict kvargs
    def call_once(self, method, params=None):
        request_json = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params or {},
            'id': self.id,
        }

        # We don't have to pass the auth token if asking for the apiinfo.version or user.checkAuthentication
        if self.auth and method != 'apiinfo.version' and method != 'user.login':
            request_json['auth'] = self.auth

        logger.debug("Sending: %s", json.dumps(request_json,
                                               indent=4,
                                               separators=(',', ': ')))
        response = self.session.post(
            self.url,
            data=json.dumps(request_json),
            timeout=self.timeout
        )
        #todo <Response [404]>
        logger.debug("Response Code: %s, %s", str(response.status_code), response.text)

        # NOTE: Getting a 412 response code means the headers are not in the
        # list of allowed headers.
        # HTTPError
        #response.raise_for_status()
        if response.status_code != 200:
            raise ZabbixAPIException('HTTP error %s: %s' %(response.status_code, response.reason))
        
        if not len(response.text):
            raise ZabbixAPIException("Received empty response")

        try:
            response_json = json.loads(response.text)
        except ValueError:
            logger.error("Unable to parse json: %s", response.text)
            response_json = {}
            raise ZabbixAPIException(
                "Unable to parse json: %s" % response.text
            )
        logger.debug("Response Body: %s", json.dumps(response_json,
                                                     indent=4,
                                                     separators=(',', ': ')))
        self.id += 1

        if 'error' in response_json:  # some exception
            if 'data' not in response_json['error']:  # some errors don't contain 'data': workaround for ZBX-9340
                response_json['error']['data'] = "No data"
            msg = u"Error {code}: {message}, {data}".format(
                code=response_json['error']['code'],
                message=response_json['error']['message'],
                data=response_json['error']['data']
            )
            raise ZabbixAPIException(msg, response_json['error']['code'])

        return response_json

    #api1 host.get' host
    def __getattr__(self, attr):
        """Dynamically create an object class (ie: host)"""
        return ZabbixAPIObjectClass(attr, self)


class ZabbixAPIObjectClass(object):
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
    
    #api1 host.get's get
    def __getattr__(self, attr):
        """Dynamically create a method (ie: get)"""

        def fn(*args, **kwargs):
            if args and kwargs:
                raise TypeError("Found both args and kwargs")
            
            return self.parent.call_once(
                '{0}.{1}'.format(self.name, attr),
                args or kwargs
            )['result']

        return fn


