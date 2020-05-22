# -*- coding: utf-8 -*-


db.define_table('services',
                Field('name', requires=IS_LOWER(), required=True, unique=True),
                Field('port', required=True, unique=True),
                )


# Ensure RDP protocol by default exits

if not db(db.services.name == 'rdp').select():
    db.services.insert(name = 'rdp',
                       port = '3389')
    
    
db.services.id.readable = False
