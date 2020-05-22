# -*- coding: utf-8 -*-
#################################################################################
# @file    ous.py
# @brief   Module that encapsulates Opengnsys Rest API and database access
#          for Opengnsys Organizational Units (OUs).   
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
#          Opengnsys Api Rest support provided by Juan Carlos García, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################

from http_requests import HttpRequest, NotUsingPoolManagerConnector
from ognsys_actions import GetLabsOu
from ados import adoDB_ous

def get_ou_credentials(db, ou_id):    
    return adoDB_ous.get_ou_credentials(db, ou_id)



# ---- Return a list of LABS (dictionary) within the passed OU ---
def get_labs(ou_id):    
    http_request = HttpRequest()
    http_request.set_connector(NotUsingPoolManagerConnector())
    labs = http_request.do_action(GetLabsOu(ou_id))
    
    
    # if not exist labs return dict {'message': 'Cannot access this resource'}
    if type(labs) is dict:
        labs = []    
    
    labs_inremote = []
    for lab in labs:
        if lab['inremotepc']:            
            labs_inremote.append(lab)
            
    return labs_inremote

# ---- Return a list of LABS (dictionary) with remotePC on ---
def get_labs_on(ou_id):
    
    labs = get_labs(ou_id)
    
    labs_on = []

    for lab in labs:        
        if lab['inremotepc'] == True:
            # No funciona api rest
                                                            
            #lab_status = __get_lab_status(str(lab['ou']['id']),str(lab['id']))             
            #lab['status'] = lab_status
                            
            labs_on.append(lab)
            
                
    return labs_on
