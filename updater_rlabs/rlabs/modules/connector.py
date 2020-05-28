# -*- coding: utf-8 -*-
#################################################################################
# @file    cnection_stage.py
# @brief   Module that manage connection stages with remotePC    
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################
from gluon import current

import json
from datetime import datetime, timedelta
import time

from client_lab import Client
from ados import adoDB_active_reserves, adoDB_openRlabs_setup
import errors


class Connection:            
        
    def __init__(self, my_context):

        self.my_context = my_context
        
        self.client = Client(self.my_context)
        
        self.WAIT_CHECK_LOOP = 10
        self.MAX_RETRIES = int((adoDB_openRlabs_setup.getSetup_OpenRLabs(my_context['db'])['seconds_to_wait'] / self.WAIT_CHECK_LOOP) - 1)
        
     
 
        
    def do_reserve(self):
        print('reserve remote PC')
        equipo_reservado= None
        # Al hacer reserva se manda arrancar el equipo y se crea entrada en cola acciones para levantar el equipo
        # deseado.
        equipo_reservado = self.client.reserve_remote_pc()

        if 'id' not in equipo_reservado:        
            return {'error': '\n ' + errors.ERROR_RESERVA}
        
        else:
            if equipo_reservado:                
                for k,v in equipo_reservado.items():
                    self.my_context[k] = v
                expiration_time = datetime.now() + timedelta(hours=
                                                             int(self.my_context.maxtime))
                expiration_time = expiration_time.strftime('%d/%m/%Y %H:%M:%S')
                
                self.my_context.expiration_time = expiration_time
                
                print('insert reserva')
                adoDB_active_reserves.insert(self.my_context)
                
                print('eventos redirigidos')
                self.client.redirect_events()
                    
                print('register timeout')            
                self.client.register_session_timeout()
                
        
                '''
                print('setup_task')
                gestor_de_reservas.setup_task(opengnsys.__OPENGNSYS_SERVER__, opengnsys.__APIKEY__, 
                                                        ou_id, lab_id, pc_id, ip, int(maxtime))
                '''            
                # Devolvemos todos los datos necesarios para poder hacer conexion a 
                # escritorio remoto.
                
                              
                equipo_reservado['client_type'] = self.my_context.client_type
                equipo_reservado['protocol'] = self.my_context.protocol
                equipo_reservado['port'] = self.my_context.port
                equipo_reservado.update({'ou_id' : self.my_context.ou_id, 'ou' : None,
                                         'lab_id': self.my_context.lab_id, 'lab' : None,
                                         'num_retries' : self.my_context.num_retries})
                
                #Por compatibilidad con el resto de la app
                #Que usa pc_id por claridad.
                equipo_reservado['pc_id'] = equipo_reservado['id']
                return {'status': '\n Reserva realizada. Equipo concedido: ' + equipo_reservado['name'] + 
                        '\n Arrancando equipo: ../',
                        'equipo_reservado': equipo_reservado}
            else:        
                return {'error': '\n Error de reserva.'}

    def check_pc_status(self):
        print('cheking..')
        ou_id = str(self.my_context.ou_id)
        lab_id = str(self.my_context.lab_id)
        pc_id = str(self.my_context.id)
        pc_name = str(self.my_context.name)
        ip = str(self.my_context.ip)
        protocol = str(self.my_context.protocol)
        port = str(self.my_context.port)
        client_type = str(self.my_context.client_type)
        
        num_retries = int(self.my_context.num_retries)
                
        if num_retries < self.MAX_RETRIES:

            time.sleep( self.WAIT_CHECK_LOOP )

            self.my_context.num_retries = str(num_retries + 1)

            pc_status = self.client.get_status_client()            

            if 'status' not in pc_status: 
                pc_status['status'] = 'error'
                
            if pc_status['status'] == 'off' or pc_status['status'] == 'oglive' \
               or pc_status['status'] == 'busy' or pc_status['status'] == 'error':
                                
                return {'status' : '.../',
                        'equipo_reservado' : self.my_context}
            else:
                
                return {'ip': ip, 'protocol': protocol, 'port': port, 
                       'pc_id': pc_id,'pc_name' : pc_name, 
                       'ou_id': ou_id, 'lab_id': lab_id,
                       'finalizado': True,
                       'client_type': client_type,
                       'status' : '\n Conexión realizada con éxito.'}
        else:        
                         
            return {'error': 'Fallo al encender el equipo de forma remota.\n Intentelo con otro equipo.'}
          
       
            