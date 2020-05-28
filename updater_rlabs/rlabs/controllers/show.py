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
from reserves import ActiveReserves
import ou
from  ados import adoDB_services, adoDB_active_reserves, adoDB_openRlabs_setup
import connector


@auth.requires_membership('enabled')
def ous():   
       
    opengnsys = Ognsys(db)
    active_reserves = ActiveReserves(db, auth.user_id, auth.user_groups.values())        
    
    check_time = adoDB_openRlabs_setup.getSetup_OpenRLabs(db)['seconds_to_wait']

    return dict(ous=opengnsys.get_ous(), 
                services=adoDB_services.get_services(db),
                maxtime_reserve = adoDB_openRlabs_setup.get_maxtime_reserve(db),
                active_reserves= active_reserves.get_reserves(),
                exits_reserves = active_reserves.exits_reserves(),
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