import smtplib
import poplib
import logging


def email_auth(server="smtp.gmail.com:587",
               domain="@gmail.com",
               tls_mode=None):
    """
    to use email_login:
    from gluon.contrib.login_methods.email_auth import email_auth
    auth.settings.login_methods.append(email_auth("smtp.gmail.com:587",
                                                  "@gmail.com"))
    """
    
    def email_auth_aux(email,
                       password,
                       server=server,
                       domain=domain,
                       tls_mode=tls_mode):
        
        if domain:
            if not isinstance(domain, (list, tuple)):                
                domain = [str(domain)]
            if not [d for d in domain if email[-len(d):] == d]:
                return False
            
        (host, port) = server.split(':')
        
        if tls_mode is None:  # then auto detect
            tls_mode = port == '587'
            
        try:
            server = None
            server = smtplib.SMTP(host, port)
            server.ehlo()
            
            if tls_mode:
                server.starttls()
                server.ehlo()
                
            server.login(email, password)
            server.quit()
            return True
        except:
            
            logging.exception('email_auth() failed')
            
            if server:
                try:
                    server.quit()
                except:  # server might already close connection after error
                    pass
                
            return False
    
    return email_auth_aux

'''    
def email_auth_pop3(server, domain, tls_mode=None):
    
    def email_auth_pop3_aux(email,
                       password,
                       server=server,
                       domain=domain,
                       tls_mode=tls_mode):
            
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
        
    return email_auth_pop3_aux
    
'''