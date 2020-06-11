# -*- coding: utf-8 -*-

email_auth_pop3 = local_import('email_auth_pop3')
from email_auth_pop3 import email_auth_pop3
from ados import adoDB_openRlabs_setup


server_info = adoDB_openRlabs_setup.get_authentication_mail_pop3_server_info(db)

name_domain = server_info['url'].split(':')[0].split('.') 
domain = name_domain[-2] + '.' + name_domain[-1]

auth.settings.login_methods = [email_auth_pop3(server_info['url'], "@" + domain, db, server_info['tls_mode'])]   
