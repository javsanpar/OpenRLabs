# -*- coding: utf-8 -*-
#################################################################################
# @file    labs.py
# @brief   Module that encapsulates Opengnsys Rest API access
#          for Opengnsys Laboratories.   
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
#          Opengnsys Api Rest support provided by Juan Carlos García, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################

import concurrent.futures
import threading
import time



import ognsys_globals
from http_requests import HttpRequest, UsingPoolManagerConnector, \
                                        NotUsingPoolManagerConnector
                                        
from ognsys_actions import GetDiskConfigClient, GetLabClients, GetStatusClient



class Lab:


    def __init__(self, ou_id, lab_id):
        self.ou_id = ou_id
        self.lab_id = lab_id
        
        
        self.http_request = HttpRequest()
          
    
    def __get_clients(self):
        self.http_request.set_connector(UsingPoolManagerConnector(ognsys_globals.local.__POOL_MANAGER__))
                
        clients = self.http_request.do_action(GetLabClients(self.ou_id, self.lab_id))
        
        try:
            return sorted(clients, key = lambda k:k['name'], reverse=True)
        except:
            return {'error': 'Error al obtener lista de clientes.'}
    
    
    # Do not use Client object to do action GetStatus for save resources.
    # Then action GestatusClient have two entry point but code is only in one place.   
    def __get_status_client(self, pc):
        self.http_request.set_connector(NotUsingPoolManagerConnector())        
        pc['status'] = self.http_request.do_action(GetStatusClient(pc['ip']))
            
        return pc
        

    def __add_status_clients(self, PCs):

        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            PCs_with_status =  list(executor.map(self.__get_status_client, PCs))
            
            print(time.time() - start_time)
            return PCs_with_status
    
     
    def __get_diskconfig_client(self, pc_id):
        self.http_request.set_connector(UsingPoolManagerConnector(ognsys_globals.local.__POOL_MANAGER__))        
        return self.http_request.do_action(GetDiskConfigClient(self.ou_id, self.lab_id, pc_id))
                        
    def __check_disponible(self, pc_status):
        if 'error' in pc_status:
            return True
        else:
            if pc_status['status'] == "off":
                return True
            else:
                return False

            
    def get_remote_clients(self):

        PCs =  self.__get_clients()
        if 'error' in PCs:
            return {'error' : 'Error de optención lista de clientes desde opengnsys'}
        if PCs:
            if len(PCs) == 0 :
                return {'error' : 'Error No quedan equipos disponibles.'}
        else:
            return {'error' : 'Error No quedan equipos disponibles.'}
        
        PCs = self.__add_status_clients(PCs)
    
        pcs_total = len(PCs)
        pcs_disponibles = 0
        PCs_info = []
        images_info = []
        #print('pcs')
        #print(PCs)
        for pc in PCs:
            # NO porque saturamos servidor opengnsys                
            #pc_status = __getStatusClient(ou_id, lab_id, str(pc['id']))
            
            #Por el momento da error si el equipo hace tiempo no levantado        
            #pc_status = __getStatusClientFromList(PCs_status, pc['id'])
            
            pc_info = {}
            
            pc_info['pc'] = pc        
            #pc_info['status'] = pc_status                
            
            PCs_info.append(pc_info)        

            if self.__check_disponible(pc['status']):

                pcs_disponibles = pcs_disponibles + 1
                
                pc_diskcfg = self.__get_diskconfig_client(str(pc['id']))
                #print('discfg')
                #print(pc_diskcfg)
                for partition in pc_diskcfg['diskcfg']:
                    #print('partition')
                    #print(partition)
                    image__aready_added = False
                                
                    if ("parttype" and 'image') in partition:
                        
                        for image in images_info:                    
                            if image['id'] == partition['image']['id']:
                                image__aready_added = True                
                        
                        if image__aready_added == False:                          
                            images_info.append({'id': partition['image']['id'], 'os': partition['os'], 
                                                'lab_id': self.lab_id, 'ou_id': self.ou_id})
        
        if len(images_info) == 0:
            return {'error' : 'Error Los equipos no tienen imagen asignada en OpenGnsys.'}
         
        if pcs_disponibles == 0:
            return {'error' : 'Error No quedan equipos disponibles'}        
        else:
            return {'PCs_info' : sorted(PCs_info, key = lambda k:k['pc']['name'], reverse=False),
                    'images_info' : images_info,
                    'disponibles_info': {'lab_id': self.lab_id,
                                         'total': pcs_total,
                                         'disponibles': pcs_disponibles}
                    }        
        
