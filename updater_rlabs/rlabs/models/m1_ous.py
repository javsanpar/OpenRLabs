# -*- coding: utf-8 -*-

db.define_table('ous_setup',
                Field('ou_id', required=True, unique=True, writable=False),
                Field('ou_name', required=True, unique=True, writable=False),                
                Field('ou_user'),
                Field('ou_password', type='password'),
                )

db.ous_setup.id.readable = False

