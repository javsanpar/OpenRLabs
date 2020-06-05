# -*- coding: utf-8 -*-
#################################################################################
# @file    email_auth_pop3.py
# @brief   Module that perform authentication again POP3 mail server    
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################
import gluon
import poplib
import logging
    
def email_auth_pop3(server, domain, db, tls_mode= None ):
    
    def email_auth_pop3_aux(email,
                       password,
                       server=server,
                       domain=domain,
                       db=db,
                       tls_mode=tls_mode):
        
        
        
        if db(db.auth_user.email == email).select():    
            (host, port) = server.split(':')
            (user) = ''.join(email).split('@')[0]
            
            
            try:            
                pop3 = None
                pop3 = poplib.POP3_SSL(host, port) if tls_mode else poplib.POP3(host, port)                
                pop3.user(user)            
                auth_response = pop3.pass_(password)
                pop3.quit()
                if "+OK" in auth_response.decode('utf-8'):    
                    return True                
                else:
                    logging.exception('email_auth() failed')
                    return False
            except:                
                logging.exception('email_auth() failed')
                if pop3:
                    try:
                        pop3.quit()
                    except:  # server might already close connection after error
                        pass                
                return False
        else:            
            return False
        
    return email_auth_pop3_aux
    
