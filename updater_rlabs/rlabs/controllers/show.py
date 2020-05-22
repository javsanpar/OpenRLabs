# -*- coding: utf-8 -*-
#################################################################################
# @file    showPCs.py
# @brief   Controller for actions connect to remote pc    
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################

import gluon # quitar en produccion. Sirve para que eclipse no de errores.
import json     
  
from gluon.storage import Storage

from ognsys import Ognsys
from lab import Lab
from client_lab import Client

import ou
from  ados import adoDB_services, adoDB_active_reserves, adoDB_openRlabs_setup
import connector


@auth.requires_membership('enabled')
def ous():   
       
    opengnsys = Ognsys(db)
    
    if 'admin' in  auth.user_groups.values():
        active_reserves = adoDB_active_reserves.getAll(db)
    else:
        active_reserves = adoDB_active_reserves.get(db, auth.user_id)   
    
    if len(active_reserves) > 0:
        exits_reserves = True
    else:
        exits_reserves = False
        
    # Render() for get user_name from id (See represent clause in model).
    # return Iterator object        
    active_reserves_iterator = active_reserves.render()
    
    # Build dict with info about status client.
    active_reserves = []
    # only oner Client whit the same PoolManager to all 
    # client status checks 
    client = Client(Storage())
    for active_reserve in active_reserves_iterator:
        
        active_reserve_dict =  active_reserve.as_dict()
        
        client.update_context({'ip' : active_reserve_dict['ip'],
                               'ou_id' : active_reserve_dict['ou_id'],
                               'lab_id' : active_reserve_dict['lab_id'],
                               })
                
        active_reserve_dict.update(client.get_status_client())
        active_reserves.append(active_reserve_dict)
    
    
    check_time = (connector.Connection.MAX_RETRIES + 1) * connector.Connection.WAIT_CHECK_LOOP

    return dict(ous=opengnsys.get_ous(), 
                services=adoDB_services.get_services(db),
                maxtime_reserve = adoDB_openRlabs_setup.get_maxtime_reserve(db),
                exits_reserves = exits_reserves,
                active_reserves=active_reserves,
                check_time = check_time
                )

@auth.requires_membership('enabled')
def labs():
    
    opengnsys = Ognsys(db)
    
    if opengnsys.set_apikey(request.post_vars.ou_id):
        
        labs_on = ou.get_labs_on(request.post_vars.ou_id)                

        return json.dumps(labs_on)
    
    else:
        return json.dumps({'error': 
                          "Error de acceso. Por favor compruebe configuración de usuario y contraseña de la OU"})

def __user_has_reserve():
    active_reserves=adoDB_active_reserves.get(db, auth.user_id)
    if len(active_reserves) > 0:
        return True
    else:
        return False

@auth.requires_membership('enabled')
def clients():    
    if (__user_has_reserve()) and (auth.has_membership(group_id='admin') == False):
        return json.dumps({'error':
                           "Tiene reservas activas. Por favor, cancelelas antes de realizar una nueva."})
    else:
        opengnsys = Ognsys(db)
        
        if opengnsys.set_apikey(request.post_vars.ou_id):
        
            lab = Lab(request.post_vars.ou_id, request.post_vars.lab_id)
            return json.dumps(lab.get_remote_clients())
        else:
            return json.dumps({'error': 
                          "Error de acceso. Por favor compruebe configuración de usuario y contraseña de la OU"})
    

@auth.requires_membership('enabled')
def unreserve():
    opengnsys = Ognsys(db)
        
    if opengnsys.set_apikey(request.post_vars.ou_id):
    
        my_context = Storage(**request.post_vars)  
        my_context['db'] = db

        client = Client(my_context)
        
        client.unreserve_remote_pc()
                
        return json.dumps({"response": "200 OK"})
    else:
        return json.dumps({"response": "500 Innternal Error"})