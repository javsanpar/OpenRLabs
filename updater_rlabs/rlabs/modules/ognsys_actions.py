# -*- coding: utf-8 -*-
#################################################################################
# @file    ognsys_actions.py
# @brief      
# @warning None
# @note Use: 
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
#          Opengnsys Api Rest support provided by Juan Carlos García, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################

import ognsys_globals

class UrlLogin:
    def __init__(self):
        self.url = ognsys_globals.local.__OPENGNSYS_SERVER__ + "/login"

    def get_url(self):
        return self.url
    
class UrlGroupOus:
    def __init__(self):
        self.url = ognsys_globals.local.__OPENGNSYS_SERVER__ + "/ous"

    def get_url(self):
        return self.url

class UrlGroupLabs:
    def __init__(self, ou_id):
        self.url = ognsys_globals.local.__OPENGNSYS_SERVER__ + "/ous/" + \
                                        str(ou_id) + "/labs"
                                        
    def get_url(self):
        return self.url


class UrlGroupClients:
    def __init__(self, ou_id, lab_id):
        self.url = ognsys_globals.local.__OPENGNSYS_SERVER__ + "/ous/" + \
                                        str(ou_id) + "/labs/" + str(lab_id) + "/clients"
                                        
    def get_url(self):
        return self.url

    
class OgnsysAction:
    def __init__(self, url_group, body = None):

        self.headers = {'Content-Type': 'application/json',
                            'Accept': 'application/json',
                            'Authorization': ognsys_globals.local.__APIKEY__,
                            'User-Agent': 'python-requests//'}
        
        self.body = body
        self.url_base = url_group.get_url()
        
        self.action = ""
        self.url = ""
        
        self.params = {}
 
    def get_params(self):
        if self.body:
            self.params['body'] = self.body
            
        self.params['action'] = self.action
        self.params['url'] = self.url
        self.params['headers'] = self.headers
        
        return self.params

class DoLogin(OgnsysAction): 
    def __init__(self, ou_credentials):
        body = {
                  "username": ou_credentials['ou_user'],
                  "password": ou_credentials['ou_password']
                }
        
        super().__init__(UrlLogin(), body)
        
        self.action = 'POST'        
        self.url = self.url_base
        
class GetOUS(OgnsysAction):            
    def __init__(self):        
        super().__init__(UrlGroupOus())
        
        self.action = 'GET'  
        print(self.action)            
        self.url = self.url_base

    

class GetLabsOu(OgnsysAction):
    def __init__(self, ou_id):
        super().__init__(UrlGroupLabs(ou_id))        
        
        self.ou_id = ou_id        
        self.action = 'GET'
        
        self.url = self.url_base

class GetLabClients(OgnsysAction):
    def __init__(self, ou_id, lab_id):
        super().__init__(UrlGroupClients(ou_id,lab_id))
                
        self.action = 'GET'        
        self.url = self.url_base
    
class GetDiskConfigClient(OgnsysAction):
    def __init__(self, ou_id, lab_id, pc_id):
        super().__init__(UrlGroupClients(ou_id,lab_id))        
        
        self.action = 'GET'                    
        self.url = self.url_base + '/' + str(pc_id) + '/diskcfg'
        
        
    
class ReserveClient(OgnsysAction):
    def __init__(self, ou_id, image_id, lab_id, maxtime):                
        body = {
                  "labid": lab_id,
                  "maxtime": int(maxtime)
                }
                
        super().__init__(UrlGroupOus(), body)
                        
        self.action = 'POST'
        self.url = self.url_base + "/" + str(ou_id) + "/images/"+ str(image_id) + "/reserve"
        
class UnreserveClient(OgnsysAction):
     def __init__(self, ou_id, lab_id, pc_id):
        
        super().__init__(UrlGroupClients(ou_id,lab_id))
        
        self.action = 'DELETE'
        self.url = self.url_base + '/' + str(pc_id) + "/unreserve"
        
        
            
        
class RedirectEvents(OgnsysAction):
    def __init__(self, ou_id, lab_id, pc_id, maxtime):        
            
        ou_id = str(ou_id)
        lab_id = str(lab_id)
        pc_id = str(pc_id)
        maxtime = str(maxtime)
        

        urlogin = ognsys_globals.local.__RLABS_SERVER__ + "/events/getEventsLogin?pc_id=" + pc_id + \
                                                                            "&lab_id=" + lab_id + \
                                                                            "&ou_id=" + ou_id + \
                                                                            "&maxtime=" + maxtime
        
        urlogout = ognsys_globals.local.__RLABS_SERVER__ + "/events/getEventsLogout?pc_id=" + pc_id + \
                                                                            "&lab_id=" + lab_id + \
                                                                            "&ou_id=" + ou_id + \
                                                                            "&maxtime=" + maxtime                                                                           
                                                                                                                                                        
        body = {
                  "urlLogin": urlogin,
                  "urlLogout": urlogout
                }
        
        super().__init__(UrlGroupClients(ou_id,lab_id), body)
        
        self.action = 'POST'
        self.url = self.url_base + '/' + pc_id + "/events"


            
class RegisterSessionTimeout(OgnsysAction):
    def __init__(self, ou_id, lab_id, pc_id, maxtime):
            
        ou_id = str(ou_id)
        lab_id = str(lab_id)
        pc_id = str(pc_id)
        maxtime = str(maxtime)
        
        deadLine = str(int(maxtime) * 60 * 60)    
        
        body ={
             "deadLine": deadLine 
        }
        
        super().__init__(UrlGroupClients(ou_id,lab_id), body)
        
        self.action = 'POST'        
        self.url = self.url_base + '/' + pc_id + "/session"




class GetStatusClient:
    def __init__(self, ip):
        self.ip = ip
    
    def get_params(self):
        params = {}
        params['action'] = 'GET'
        params['url'] = "https://" + self.ip + ":8000/opengnsys/status"
        params['headers'] =  {'Content-Type': 'application/json',
                            'Accept': 'application/json',
                            'User-Agent': 'python-requests//'}
        

        return params
            
     