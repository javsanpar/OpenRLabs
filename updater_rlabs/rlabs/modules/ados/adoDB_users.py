# -*- coding: utf-8 -*-
#################################################################################
# @file    adoDB_users.py
# @brief   Module that manage database info about OpenRemoteLabs Users.   
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################
def get_users(db):
    return (db.auth_user.id>0)

def get_users_menbership(db):
    return (db.auth_membership.id>0)

def insert_user(db, first_name, last_name, email ):
    db.auth_user.insert(first_name=first_name,
                           last_name=last_name,
                           email=email,
                           registration_id=email)
    db.commit()

def remove_users(db,users_id):
    if users_id:
        for user_id in users_id:
            print(user_id)
            db(db.auth_user.id == user_id).delete()
        
        db.commit()
    