# -*- coding: utf-8 -*-
#################################################################################
# @file    opengngys.py
# @brief   Module that get and store credential for access Rest API opengnsys and 
#          get Opengnsys OUs. Suply global access to server opengnsys entity.
#          import vs singleton pattern.
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
#          Opengnsys Api Rest support provided by Juan Carlos García, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################

from http_requests import HttpRequest, UsingPoolManagerConnector
from ognsys_actions import DoLogin
import threading
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


import ou
import adoDB_openRlabs_setup
import adoDB_ous


local = threading.local()
local.__OPENGNSYS_SERVER__ = ""
local.__RLABS_SERVER__ = ""
local.__APIKEY__ = ""
local.__OU__ = ""

# Used to avoid refactor all dependecies
__OPENGNSYS_SERVER__ = local.__OPENGNSYS_SERVER__
__RLABS_SERVER__ = local.__RLABS_SERVER__

__APIKEY__ = local.__APIKEY__


_current_ou = local.__OU__

__POOL_MANAGER__ = urllib3.PoolManager(num_pools=10, maxsize=10, 
                                       cert_reqs='CERT_NONE',
                                       assert_hostname=False)
        
class Ognsys:
        
    def __init__(self, db, ou_id = None):
        self.db = db
        self.ou_id = ou_id
        
        self.http_request = HttpRequest()

        
        self.__setServers(db)
        
        global _current_ou

        if ou_id and _current_ou != ou_id:
            
            _current_ou = ou_id
    
            credentials = self.doLogin()
            if 'apikey' in credentials:
                self.setApiKey(credentials['apikey'])
                
                return True
            else:
                return False
            
        return True
    
    def __setServers(self):                
        global local
        local.__OPENGNSYS_SERVER__ = adoDB_openRlabs_setup.get_openGnsys_server(self.db)
        
        local.__RLABS_SERVER__ = adoDB_openRlabs_setup.get_openRLabs_server(self.db)
    
        
    def setApiKey(self):
        global __APIKEY__
        __APIKEY__ = apikey
    
    # ---- Do Login and return dictionary with UserID  and ApiKey ---        
    def doLogin(self):
        self.http_request.set_connector(UsingPoolManagerConnector(opengnsys.__POOL_MANAGER__))        
        return self.http_request.do_action(DO(self.ou_id, self.lab_id, pc_id))
        
        recurso = __OPENGNSYS_SERVER__ + "/login"
    
        # Usar usuario propietario de la OU (Unidad Organizativa)
        
        ou_credentials = ou.get_ou_credentials(self.db, self.ou_id)
        parametros = {
                  "username": ou_credentials['ou_user'],
                  "password": ou_credentials['ou_password']
                }
        http_manager = PoolManager()
        return http_manager.doPOST(recurso, parametros, __APIKEY__)
        
    def getDiskConfigClient_params():
        params = {}    
        return params
    
    def get_http_params(action):
        print(action.__name__)
        if action.__name__ == 'GetDiskConfigClient':
            return getDiskConfigClient_params()    
                
    # ---- Return a list of dictionaries {OU_ID: OU_NAME} ---
    def getOUS():
        recurso = __OPENGNSYS_SERVER__ + "/ous"
        http_manager = PoolManager()
        return http_manager.doGET(__APIKEY__, recurso)        
    
    
    
    def update_ous_in_table(db, ou):
        adoDB_ous.update_ous_in_table(db, ou)
    
           
    def delete_ous_not_in_ous_server(db, ou):
        adoDB_ous.delete_ous_not_in_ous_server(db, ou)
                
                
    def synchronize_table_OUs(db):
        ou = getOUS()
        adoDB_ous.update_ous_in_table(db, ou)        
        adoDB_ous.delete_ous_not_in_ous_server(db, ou)    
        
        
    def get_queryOUs(db):
        return adoDB_ous.get_queryOUs(db)
        
