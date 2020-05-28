# -*- coding: utf-8 -*-
#################################################################################
# @file    connectPC.py
# @brief   Controller actions to connect remote pc    
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


from connector import Connection
from ognsys import Ognsys
from client_lab import Client

from ados import adoDB_openRlabs_setup
import ports_manager
import logger

@auth.requires_membership('enabled')   
def do_reserve():          
    if request.post_vars:
                
        opengnsys = Ognsys(db)    
        if opengnsys.set_apikey(request.post_vars.ou_id):
                     
            my_context = Storage(**request.post_vars)  
            my_context['db'] = db
            my_context['user_id'] = auth.user_id
            my_context['num_retries'] = 0
            
            connection = Connection(my_context)
            
            reserve = connection.do_reserve()
            
            logger.log(auth.user.first_name, auth.user.last_name,
                       reserve['equipo_reservado']['name'], reserve['equipo_reservado']['ip'], "do_reserve")
            
            return json.dumps(reserve)
        else:
            return json.dumps({'error', 'Error de inicialización, compruebe configuración opengnsys'})
    else:        
        return json.dumps({'error', 'Error haciendo reserva status'})
    
@auth.requires_membership('enabled')      
def check_pc_status():
    print('check_status')
    if request.post_vars:
                                
        opengnsys = Ognsys(db)
        if opengnsys.set_apikey(request.post_vars.ou_id):
            
            my_context = Storage(**request.post_vars)  
                
            my_context['db'] = db
                    
            connection = Connection(my_context)  
            pc_status_info = connection.check_pc_status()
            if 'error' in pc_status_info:
                print('unreserve')

                                
                client = Client(my_context)
                
                client.unreserve_remote_pc()
                
                logger.log(auth.user.first_name, auth.user.last_name,
                       request.post_vars.name, request.post_vars.ip, "reserve_error")
            
                              
            # Key db raise error in json.load
            if 'equipo_reservado' in pc_status_info:
                if 'db' in pc_status_info['equipo_reservado']:        
                    pc_status_info['equipo_reservado']['db'] = None
            
            return json.dumps(pc_status_info)
        else:
            return json.dumps({'error', 'Error de inicialización, compruebe configuración opengnsys'})
    else:
        return json.dumps({'error', 'Error chequeando status'})
        
            
@auth.requires_membership('enabled')   
def desktop():        
    if request.vars != None:
        logger.log(auth.user.first_name, auth.user.last_name,
                   request.vars.pc_name, request.vars.ip, "remote_desktop")
        
        return dict(ip=request.vars.ip, pc_name=request.vars.pc_name,
                protocol=request.vars.protocol, port=request.vars.port, username="",
                ou_id = request.vars.ou_id, lab_id = request.vars.lab_id, pc_id = request.vars.pc_id,
                url_webSocket = adoDB_openRlabs_setup.get_Apache_Guacamole_WebSocket(db))

@auth.requires_membership('enabled')   
def openport():
    print("abriremos puertos")
    print(request.post_vars)    
    port = ports_manager.get_origin_port(request.client, request.post_vars.ip_remote, 
                                              request.post_vars.port_remote, request.post_vars.maxtime)    
    
    return json.dumps({'port': port})

