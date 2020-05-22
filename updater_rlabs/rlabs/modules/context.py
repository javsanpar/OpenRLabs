# -*- coding: utf-8 -*-
#################################################################################
# @file    global_context.py
# @brief   Module that store all objects of connection (remote_pc_data, db, ...etc).    
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2020-02-04
#################################################################################

from gluon.storage import Storage


class Context():
    
    def __init__(self):
        self.context = Storage()
    
    
def add_context(**kwargs):
    #print('adding context')
    #print(kwargs)
    global __context
    
    if kwargs:
        __context.update(kwargs)
    
def get_context(*args):
    return_objects = {}
    if args:
        if len(args) > 1:
            for obj in args:
                return_objects.update({obj : __context[obj]})
            return return_objects
        else:
            return __context[args[0]]
    else:            
        return __context 
    
    