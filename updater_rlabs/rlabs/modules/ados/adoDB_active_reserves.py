# -*- coding: utf-8 -*-
#################################################################################
# @file    adoDB_active_reserves.py
# @brief   Module that manage database info about available services (rdp, vnc, ...etc.)   
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################

def get(db, auth_id):
    return db(db.active_reserves.user_id == auth_id).select()

def getAll(db):
    return db(db.active_reserves.id > 0).select()

def remove_reserve(db, reserve_id):
    deleted = db(db.active_reserves.id == reserve_id).delete()
    db.commit()
    return  deleted

def remove_by_pc_id(db, pc_id):
    deleted = db(db.active_reserves.pc_id == pc_id).delete()
    db.commit()
    return  deleted


    
def insert(my_context):
    db = my_context.db
    reserve_id = db.active_reserves.insert(user_id = int(my_context.user_id),
                                     ou_id = str(my_context.ou_id),
                                     lab_id = str(my_context.lab_id),
                                     pc_id = str(my_context.id),
                                     pc_name = str(my_context.name),
                                     expiration_time = my_context.expiration_time,
                                     ip = str(my_context.ip),
                                     protocol = str(my_context.protocol),
                                     port = str(my_context.port),
                                    )
    db.commit()
    return reserve_id