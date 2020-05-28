# -*- coding: utf-8 -*-
#################################################################################
# @file    clients.py
# @brief   Module that manage info about clients (remote PCs), from Opengnsys API Rest    
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
#          Opengnsys Api Rest support provided by Juan Carlos García, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################

from http_requests import HttpRequest, UsingPoolManagerConnector, NotUsingPoolManagerConnector
from ognsys_actions import GetStatusClient, ReserveClient, RedirectEvents, RegisterSessionTimeout, UnreserveClient

import ognsys_globals
from ados import adoDB_active_reserves

class Client:
    
    def __init__(self, my_context):
        self.context = my_context
        
        self.http_request = HttpRequest()
 
    
    def update_context(self, *args):
        if args:
            for arg in args:
                self.context.update(arg)
            
            
        
    # Meter este metodo en  objeto client_lab y pasarle pool manager.    
    def get_status_client(self):
        self.http_request.set_connector(NotUsingPoolManagerConnector())        
        return self.http_request.do_action(GetStatusClient(self.context.ip))
            


    def reserve_remote_pc(self):
        self.http_request.set_connector(UsingPoolManagerConnector(ognsys_globals.local.__POOL_MANAGER__))        
        return self.http_request.do_action(ReserveClient(self.context.ou_id,
                                                         self.context.image_id,
                                                         self.context.lab_id,
                                                         self.context.maxtime) )
                    
    def redirect_events(self):
        self.http_request.set_connector(UsingPoolManagerConnector(ognsys_globals.local.__POOL_MANAGER__))
        return self.http_request.do_action(RedirectEvents(self.context.ou_id, self.context.lab_id,
                                                          self.context.id, self.context.maxtime) )
                                                          
    def register_session_timeout(self):
        self.http_request.set_connector(UsingPoolManagerConnector(ognsys_globals.local.__POOL_MANAGER__))     
        return self.http_request.do_action(RegisterSessionTimeout(self.context.ou_id, self.context.lab_id, 
                                                                  self.context.id, self.context.maxtime) )

    
                                                        
        
    
    def __unreserve_remote_pc(self):
        self.http_request.set_connector(UsingPoolManagerConnector(ognsys_globals.local.__POOL_MANAGER__))     
        return self.http_request.do_action(UnreserveClient(self.context['ou_id'], self.context['lab_id'], self.context['pc_id']))
        
    
    def unreserve_remote_pc(self):
        
        self.remove_active_reserve()
        
        unreserve_ognsys = self.__unreserve_remote_pc()                
        
        return unreserve_ognsys
        
    def remove_active_reserve(self):

        adoDB_active_reserves.remove_by_pc_id(self.context.db, self.context.pc_id)
        return "ok"
        
