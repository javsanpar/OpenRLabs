# -*- coding: utf-8 -*-
#################################################################################
# @file    adoDB_ous.py
# @brief   Module that manage database info about Opengnsys Organitational Untis (OUs).   
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################

##############################################################################
# Modulo encargado de gestionar info sobre ou en BBDD
##############################################################################

def get_ou_credentials(db, ou_id):    
    return (db(db.ous_setup.ou_id == ou_id).select().first())


def update_ous_in_table(db, ous):
    
    for ou in ous:
        if db(db.ous_setup.ou_name == ou['name']).count() == 0:
            db.ous_setup.update_or_insert(db.ous_setup.ou_id == ou['id'],
                                      ou_id = ou['id'],
                                      ou_name = ou['name'])
    db.commit()
            
def delete_ous_not_in_ous_server(db, ous):
    ous_table = db(db.ous_setup.id > 0).select()
    for ou_table in ous_table:
        exist = False
        for ou in ous:  
                      
            if  ou['id'] == int(ou_table.ou_id) :
                exist = True
                        
        if exist == False:
            ou_table.delete_record()
            
    db.commit()
      
def get_queryOUs(db):
    return (db.ous_setup.id>0)
        