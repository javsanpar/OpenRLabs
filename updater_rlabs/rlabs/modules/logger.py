# -*- coding: utf-8 -*-
#################################################################################
# @file    logger.py
# @brief   Class for create openrlabs logs    
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################

import logging
from logging.handlers import TimedRotatingFileHandler 

# create logger with 'spam_application'
logger = logging.getLogger('openrlabs')
logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
#fh = logging.FileHandler('logs/openrlabs.log')
fh = logging.handlers.TimedRotatingFileHandler('logs/openrlabs.log', 'midnight', 1, 7)
fh.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
        
def log(first_name, last_name, pc_name, pc_ip, action):
    if action == "remote_desktop":
        msg_action = " connected to Desktop "
    if action == "do_reserve":
        msg_action = " get a reserve for "
    if action == "reserve_error":
        msg_action = " error in reserve "
        
    msg = first_name + " " + last_name + msg_action + pc_name + " " + pc_ip
    logger.info(msg)