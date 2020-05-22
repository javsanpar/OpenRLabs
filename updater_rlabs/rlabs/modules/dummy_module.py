import time
from random import randint
import threading



_var_global = None

_local = threading.local()

def set_var(var):
    global _var_global
    _var_global = var
    global _local
    _local.var = var
    
    time.sleep(randint(10,20))

    print('Module var pasada ' + str(var) + \
              ' local var ' + str(_local.var) + \
              ' non local ' + str(_var_global))