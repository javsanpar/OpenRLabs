# -*- coding: utf-8 -*-
#################################################################################
# @file    reserves.py
# @brief   
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
#          Opengnsys Api Rest support provided by Juan Carlos García, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################

from gluon.storage import Storage

from client_lab import Client
from ados import adoDB_active_reserves

class ActiveReserves:
    def __init__(self, db, user_id,  user_groups):        
        self.db = db
        self.user_id = user_id
        self.user_groups = user_groups
        # Contains info about status client.
        self.active_reserves = [] 
        self.__set_reserves()
        
    def __set_reserves(self):

        if 'admin' in  self.user_groups:
            active_reserves = adoDB_active_reserves.getAll(self.db)
        else:
            active_reserves = adoDB_active_reserves.get(self.db, self.user_id)   
        
        # Render() for get user_name from id (See represent clause in model).
        # return Iterator object        
        active_reserves_iterator = active_reserves.render()
        
        client = Client(Storage())
        
        for ar in active_reserves_iterator:
            
            ar_dict =  ar.as_dict()
            
            client.update_context({'ip' : ar_dict['ip'],
                                   'ou_id' : ar_dict['ou_id'],
                                   'lab_id' : ar_dict['lab_id'],
                                   })
                    
            ar_dict.update(client.get_status_client())
            
            self.active_reserves.append(ar_dict)
            
            
    def get_reserves(self):
        return self.active_reserves
    
    def exits_reserves(self):

        if len(self.active_reserves) > 0:
            return True
        else:
            return False
