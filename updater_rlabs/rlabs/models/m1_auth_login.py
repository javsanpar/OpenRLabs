# -*- coding: utf-8 -*-

email_auth_pop3 = local_import('email_auth_pop3')
from email_auth_pop3 import email_auth_pop3
from ados import adoDB_openRlabs_setup


server = adoDB_openRlabs_setup.get_authentication_mail_pop3_server(db)
name_domain = server.split(':')[0].split('.') 
domain = name_domain[-2] + '.' + name_domain[-1]


auth.settings.login_methods = [email_auth_pop3(server, "@" + domain, db)]   
