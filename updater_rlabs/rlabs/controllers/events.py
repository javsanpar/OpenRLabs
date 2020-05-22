# -*- coding: utf-8 -*-
#################################################################################
# @file    events.py
# @brief   Controller for clients events    
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################
# -------------------------------------------------------------------------
# Controller for clients events
# -------------------------------------------------------------------------
import gluon # quitar en produccion. Sirve para que eclipse no de errores.

from gluon.storage import Storage


from ognsys import Ognsys
from client_lab import Client
from ados import adoDB_active_reserves

def getEventsLogin():
    print('Evento producido: login')
    #print(request.vars.pc_id)
    '''    
    parametros_sesion_registrados = clients.register_session_timeout(request.vars.ou_id, 
                                                              request.vars.lab_id,                                          
                                                              request.vars.pc_id,
                                                              request.vars.maxtime)
    '''
    
    #print(parametros_sesion_registrados)        
        

def getEventsLogout():
    print('Evento producido: logout')
    
    opengnsys = Ognsys(db)    
    if opengnsys.set_apikey(request.post_vars.ou_id):  
             
        my_context = Storage(**request.vars)  
        my_context['db'] = db
        
        client = Client(my_context)        
        client.unreserve_remote_pc()
        
    else:
        print({'error' : 'Error de inicialización'})
    
    
def getEventsWindowUnload():    
    print('Evento producido: Window Unload (closed, refresh, others')
        
        