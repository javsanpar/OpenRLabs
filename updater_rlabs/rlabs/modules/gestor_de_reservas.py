# -*- coding: utf-8 -*-
#################################################################################
# @file    gestor_de_reservas.py
# @brief   Module that work with the scheduler service (rdp, vnc, ...etc.)   
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################

########################################################################
##### task running by scheduler worker                             #####
##### we need initialice opengnys module values                    #####
########################################################################

from gluon import current
from datetime import timedelta as timed, datetime

import client

__MINUTOS_RESTANTES__ = 1
__TMP_MINUTOS_RESERVA__ = 5

def unreserve(__OPENGNSYS_SERVER__, __APIKEY__,ou_id, lab_id, pc_id):
    client.unreserveRemotePC(ou_id, lab_id, pc_id,__OPENGNSYS_SERVER__, __APIKEY__)        
    
def send_poweroff(ip, __APIKEY__):
    client.send_poweroff(ip, __APIKEY__)

def setup_task(__OPENGNSYS_SERVER__, __APIKEY__, ou_id, lab_id, pc_id, ip, maxtime):        
    ## habra que cambiar timed(seconds=30) por timed(hours=maxtime)    
    #current.scheduler.queue_task('send_poweroff',[ip, __APIKEY__],
    #                            start_time=datetime.now() + timed(minutes=__TMP_MINUTOS_RESERVA__))    
    
    current.scheduler.queue_task('unreserve',[__OPENGNSYS_SERVER__, __APIKEY__,ou_id, lab_id, pc_id],
                                start_time=datetime.now() + timed(hours=maxtime))
    
    

