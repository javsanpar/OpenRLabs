# -*- coding: utf-8 -*-
#################################################################################
# @file    adoDB_services.py
# @brief   Module that manage database info about available services (rdp, vnc, ...etc.)   
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################
def get_services_query(db):
    return (db.services.id>0)

def get_services(db):
    return db(db.services.id>0).select()