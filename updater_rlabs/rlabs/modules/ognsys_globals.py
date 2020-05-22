# -*- coding: utf-8 -*-
#################################################################################
# @file    ognsys_servers.py
# @brief   Module that store global info to access Rest API opengnsys.
#          Suply global access using import vs singleton pattern.
#          With threading.local() ensure one var per threading/Http Requests
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
#          Opengnsys Api Rest support provided by Juan Carlos García, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################


import threading
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from ados import adoDB_openRlabs_setup


local = threading.local()


        
def init(db):
    # Don't do 'local' var inittialization in module import beacause module is
    # imported only first time server thread is launch.
     
    global local
    local.__OPENGNSYS_SERVER__ = adoDB_openRlabs_setup.get_openGnsys_server(db)
    
    local.__RLABS_SERVER__ = adoDB_openRlabs_setup.get_openRLabs_server(db)
    
    # Global Request/Thread  PoolManager 
    
    local.__POOL_MANAGER__ = urllib3.PoolManager(num_pools=10, maxsize=10, 
                                           cert_reqs='CERT_NONE',
                                           assert_hostname=False)
    
    # Do init __APIKEY__ because import do only first time
    # and var local is new each request.
    
    local.__APIKEY__ = ""
            


def set_servers(db):                
    global local
    local.__OPENGNSYS_SERVER__ = adoDB_openRlabs_setup.get_openGnsys_server(db)
    
    local.__RLABS_SERVER__ = adoDB_openRlabs_setup.get_openRLabs_server(db)
    
    # Do init __APIKEY__ because import do only first time
    # and var local is new each request.
    
    local.__APIKEY__ = ""
    
def set_apikey(apikey):
    global local
    local.__APIKEY__ = apikey

