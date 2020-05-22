# -*- coding: utf-8 -*-
'''
from gluon import current

from gluon.scheduler import Scheduler

from  gestor_de_reservas import unreserve, send_poweroff

current.scheduler = Scheduler(db, tasks=dict(unreserve=unreserve, send_poweroff=send_poweroff),
                              discard_results=False)


'''
