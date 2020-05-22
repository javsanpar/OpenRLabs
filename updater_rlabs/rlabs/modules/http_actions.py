# -*- coding: utf-8 -*-
#################################################################################
# @file    http_actions.py
# @brief      
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
import opengnsys

requests.packages.urllib3.disable_warnings() 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


        
class PoolManager:
    def __init__(self):

        # Using such a timeout and retries setup to secure that: check PC is ON, with __doGET() method, 
        # is trying it during 5 minutes aprox.
     
        self.manager = urllib3.PoolManager(num_pools=10, maxsize=10, cert_reqs='CERT_NONE',
                            assert_hostname=False)




    def doGET(self, __APIKEY__, recurso, timeout=0.05, retries = 1, redirect = 1):     
        try:  
            respuesta_json = self.manager.request(
                                    'GET',
                                    recurso,
                                    headers={'Accept': 'application/json',
                                             'Authorization': __APIKEY__},
                                    timeout=timeout, retries=retries, redirect=redirect)                
            
            return json.loads(respuesta_json.data.decode('utf-8'))
        except urllib3.exceptions.MaxRetryError:        
            return {'error': 'Error de conexión.'}
        
    def doGET_request(self,__APIKEY__, recurso, timeout=0.05, allow_redirects = False):     
        try:  
            respuesta = requests.get(recurso,
                                    headers={'Accept': 'application/json',
                                             'Authorization': __APIKEY__},
                                    verify=False,
                                    timeout=timeout, 
                                    allow_redirects=allow_redirects)                
            return json.loads(respuesta.text)
        except requests.exceptions.RequestException :        
            return {'error': 'Error de conexión.'}
        
        
    
    def doDELETE(self, __APIKEY__, recurso, timeout=1, retries = 1, redirect = 1):    
        respuesta_json = self.manager.request(
                                'DELETE',
                                recurso,
                                headers={'Accept': 'application/json',
                                         'User-Agent': 'python-requests//',
                                         'Authorization': __APIKEY__},
                                timeout=timeout, retries=retries, redirect=redirect)        
    
        return json.loads(respuesta_json.data.decode('utf-8'))
    
             
    def doPOST(self, recurso, parametros, apikey, timeout=1, retries = 1, redirect = 1):
        parametros_json = json.dumps(parametros).encode('utf-8')
        
        respuesta_json = self.manager.request(
                            'POST',
                            recurso,
                            body = parametros_json,
                            headers={'Content-Type': 'application/json',
                                     'Accept': 'application/json',
                                     'Authorization': apikey,
                                     'User-Agent': 'python-requests//'},
                            timeout=timeout, retries=retries, redirect=redirect)
                    
        return json.loads(respuesta_json.data.decode('utf-8'))    