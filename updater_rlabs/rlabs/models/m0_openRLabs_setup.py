# -*- coding: utf-8 -*-

db.define_table('openRLabs_setup',
                Field('URL_Apache_Guacamole_WebSocket', required=True),
                Field('URL_openGnsys_server', required=True),
                Field('URL_openRLabs_server', required=True),
                Field('URL_authentication_mail_pop3_server', required=True),
                Field('maxtime_reserve', required=True, default='2'),
                Field('seconds_to_wait', required=True, default=200)
                )

if db(db.openRLabs_setup).isempty():
    import load_init_setup
    
    load_init_setup.load_setup(db)
    
#Ensure only one record
first = db(db.openRLabs_setup.id > 1).select().first()

if first:
    db(db.openRLabs_setup.id != first['id']).delete()
    
db.openRLabs_setup.id.readable = False

