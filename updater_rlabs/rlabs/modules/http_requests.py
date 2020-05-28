# -*- coding: utf-8 -*-
#################################################################################
# @file    http_requests.py
# @brief   Module that implement strategy pattern to do http request   
# @warning None
# @note Use: 
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
#          Opengnsys Api Rest support provided by Juan Carlos García, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################
import urllib3
import json
import requests

requests.packages.urllib3.disable_warnings() 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import errors

class UsingPoolManagerConnector:
    def __init__(self, pool_manager):
        self.pool_manager = pool_manager
        self.TIMEOUT = 0.05
        self.TIMEOUT_POST = 1
        
    def do_action(self, action):
        params = action.get_params()
        
        try:  
            respuesta_json = self.__do_request(params)                
            
            return json.loads(respuesta_json.data.decode('utf-8'))
        except urllib3.exceptions.MaxRetryError:        
            return {'error': errors.ERROR_CONEXION}        
    
    def __do_request(self, params):
        param_request = [params['action'], params['url']]
                
        if params['action'] == 'GET':
            timeout = self.TIMEOUT
            
        if params['action'] == 'POST' or params['action'] == 'DELETE' :
            timeout = self.TIMEOUT_POST
        
         
        if 'body' in params:
           
            return self.pool_manager.request(*param_request, 
                                             body = json.dumps(params['body']).encode('utf-8'), 
                                             headers = params['headers'],
                                             timeout = timeout, retries=1, redirect=1)
        else:
            return self.pool_manager.request(*param_request, headers = params['headers'],
                                             timeout = timeout, retries=1, redirect=1)
        
class NotUsingPoolManagerConnector:
    def __init__(self):
        self.TIMEOUT = 0.05
        self.TIMEOUT_POST = 1
        
    def do_action(self, action):

        params = action.get_params()

        try:  
            respuesta = self.__do_request(params)
            return json.loads(respuesta.text)
        except requests.exceptions.RequestException :        
            return {'error': errors.ERROR_CONEXION}
        
    def __do_request(self, params):
        
        if params['action'] == 'GET':
            timeout = self.TIMEOUT
        else:
            timeout = self.TIMEOUT_POST
            
        return requests.get(params['url'],
                                        headers=params['headers'],
                                        verify=False,
                                        timeout=timeout, 
                                        allow_redirects=False)  
            
        

class HttpRequest:
    def __init__(self, connector = None):     
        
        self.connector = connector
        
    def set_connector(self, connector):
        self.connector = connector
        
    def do_action(self, action):
        return self.connector.do_action(action)
        
