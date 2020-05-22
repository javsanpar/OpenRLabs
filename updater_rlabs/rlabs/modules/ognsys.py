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

import threading


from http_requests import HttpRequest, UsingPoolManagerConnector
from ognsys_actions import DoLogin, GetOUS
import ognsys_globals
import ou
from ados import adoDB_ous

        
class Ognsys:
        
    def __init__(self, db):
        self.db = db
        
        ognsys_globals.init(db)

        
        self.http_request = HttpRequest()

    # ---- Return a list of dictionaries {OU_ID: OU_NAME} ---
    def get_ous(self):
        self.http_request.set_connector(UsingPoolManagerConnector(ognsys_globals.local.__POOL_MANAGER__))        
        return self.http_request.do_action(GetOUS())

        
    def set_apikey(self, ou_id):
        
        ou_credentials = ou.get_ou_credentials(self.db, ou_id)

        self.http_request.set_connector(UsingPoolManagerConnector(ognsys_globals.local.__POOL_MANAGER__))        
        credentials = self.http_request.do_action(DoLogin(ou_credentials))

        if 'apikey' in credentials:
            ognsys_globals.set_apikey(credentials['apikey'])

            return True
        else:

            return False
                
                
    def synchronize_table_ous(self, db):
        ou = self.get_ous()
        adoDB_ous.update_ous_in_table(db, ou)        
        adoDB_ous.delete_ous_not_in_ous_server(db, ou)    
        
        
    def get_query_ous(self, db):
        return adoDB_ous.get_queryOUs(db)
        
