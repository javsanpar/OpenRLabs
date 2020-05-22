# -*- coding: utf-8 -*-
from datetime import datetime

db.define_table('active_reserves',
                Field('user_id', 'reference auth_user', required=True,
                      requires = IS_IN_DB(db, db.auth_user.id, '%(first_name)s'),
                      represent=lambda id, result: db.auth_user[id].first_name + " " +
                                                   db.auth_user[id].last_name
                                                   ),
                Field('ou_id', required=True),
                Field('lab_id', required=True),
                Field('pc_id', required=True),
                Field('pc_name', required=True),
                Field('expiration_time', 'datetime', required=True),
                Field('ip', required=True),
                Field('protocol', required=True),
                Field('port', required=True),
                )

# Remove all expired reserves
db(db.active_reserves.expiration_time < datetime.now()).delete()
