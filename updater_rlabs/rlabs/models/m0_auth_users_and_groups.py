# -*- coding: utf-8 -*-

db.auth_user.id.readable = False
db.auth_user.password.readable = False
db.auth_user.password.writable = False

db.auth_user.email.unique = True # Only works on forms


db.auth_membership.id.readable = False

  
def enable_user(row, id):
    enabled_id = db(db.auth_group.role == 'enabled').select().first()['id']
    db.auth_membership.insert(user_id = id,
                              group_id = enabled_id)



db.auth_user._after_insert.append(lambda row, id: enable_user(row, id))
