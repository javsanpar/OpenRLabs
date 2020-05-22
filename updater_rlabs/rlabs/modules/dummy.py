
import time
from random import randint
import threading

class Singleton(type):
    instance = None
    def __call__(cls, *args, **kw):
        if not cls.instance:
             cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


class DummySingleton(metaclass=Singleton):
    
    def __init__(self):
        self.var = None
        self.local = threading.local()
        print(self)
        
    def set_var(self, var):
        self.local.var = var
        self.var = var
                
        #print('my var' + str(self.local.var))
        time.sleep(randint(10,20))
        print('Singleton var pasada ' + str(var) + \
              ' local var ' + str(self.local.var) + \
              ' non local ' + str(self.var))
          
class Dummy:
    
    def __init__(self):
        self.var = None
        self.local = threading.local()
        print(self)
        
    def set_var(self, var):
        self.local.var = var
        self.var = var
                
        #print('my var' + str(self.local.var))
        time.sleep(randint(10,20))
        print('var pasada ' + str(var) + \
              ' local var ' + str(self.local.var) + \
              ' non local ' + str(self.var))
