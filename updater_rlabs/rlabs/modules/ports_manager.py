# -*- coding: utf-8 -*-
#################################################################################
# @file    ports_manager.py
# @brief   Add an remove iptables rules and get one  
#          input free port.
# @warning None
# @note Use: IPTABLES to manage NAT ports.
#            AT to schedule ports allowance time.   
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza,
#          Opengnsys Api Rest support provided by Juan Carlos García, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################
import subprocess
import re


def get_origin_port(ip_origin, ip_remote, port_remote, maxtime):
    new_port = search_new_port()
    add_iptables_rules(ip_origin, ip_remote, new_port, port_remote)
    schedule_delete_rules(ip_origin, ip_remote, new_port, port_remote, maxtime)
    return new_port

def search_new_port():
    ports_in_use = get_ports_in_use()
    port = 11000
    port_range = 4000
    for i in range(port_range):
        if port in ports_in_use:
            port = port + 1
        else:
            break            
        
    return str(port)


def add_iptables_rules(ip_origin, ip_remote, new_port, port_remote):
    rules = iptables_rules(ip_origin, ip_remote, new_port, port_remote, "A")
    for rule in rules:        
        subprocess.run(rule, shell=True)
        
    
def iptables_rules(ip_origin, ip_remote, new_port, port_remote, action):
    return ["sudo iptables -t nat -" + action + " PREROUTING -s " + ip_origin + " -p tcp --dport " + new_port  + \
                " -j DNAT --to-destination " + ip_remote + ":" + port_remote,
            "sudo iptables -t nat -" + action + " POSTROUTING -s " + ip_origin + \
                   " -p tcp -d " + ip_remote + " -j MASQUERADE",
            "sudo iptables -" + action + " FORWARD -s " + ip_origin + " -d " + ip_remote +" -p tcp -j ACCEPT"]
    

def schedule_delete_rules(ip_origin, ip_remote, new_port, port_remote, maxtime):
    rules = iptables_rules(ip_origin, ip_remote, new_port, port_remote, "D")
    repeated_nat = check_repeat_nat_rules(ip_origin, ip_remote)
    repeated_forward = check_repeat_forward_rules(ip_origin, ip_remote)
    for i in range(repeated_nat['repeated_DNAT']):
        subprocess.run('echo ' + rules[0] + ' | sudo at now + ' + maxtime + ' hours', shell=True)
    for i in range(repeated_nat['repeated_MASQUERADE']):
        subprocess.run('echo ' + rules[1] + ' | sudo at now + ' + maxtime + ' hours', shell=True)
    for i in range(repeated_forward):
        subprocess.run('echo ' + rules[2] + ' | sudo at now + ' + maxtime + ' hours', shell=True)
    

def check_repeat_nat_rules(ip_origin, ip_remote):        
    iptables = subprocess.run('sudo iptables -t nat -L', shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
    repeated_DNAT = 0  
    repeated_MASQUERADE = 0      
    for line in iptables.splitlines():        
        line_splited = re.sub(' +', ' ', line).split(' ')
        target = line_splited[0]        
        if target == 'DNAT':
            source = line_splited[3]
            destiny= line_splited[-1].split(':')[1]
            if source == ip_origin and destiny == ip_remote:
                repeated_DNAT = repeated_DNAT + 1                
                
        
        if target == 'MASQUERADE':
            source = line_splited[3]
            destiny = line_splited[4]
            if source == ip_origin and destiny == ip_remote:
                repeated_MASQUERADE = repeated_MASQUERADE + 1                
    
    return {'repeated_DNAT':repeated_DNAT, 'repeated_MASQUERADE':repeated_MASQUERADE}
        
def check_repeat_forward_rules(ip_origin, ip_remote):        
    iptables = subprocess.run('sudo iptables -L', shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
    repeated = 0        
    for line in iptables.splitlines():        
        line_splited = re.sub(' +', ' ', line).split(' ')        
        if len(line_splited) > 5:
            source = line_splited[3]
            destiny = line_splited[4]
            if source == ip_origin and destiny == ip_remote:
                repeated = repeated + 1                
    
    return repeated        
    
def get_ports_in_use():    
    iptables = subprocess.run('sudo iptables -t nat -L', shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
    ports = []
    for line in iptables.splitlines():        
        line_splited = re.sub(' +', ' ', line).split(' ')        
        target = line_splited[0]                
        if target == 'DNAT':
            ports.append(int(line_splited[-2].split(':')[-1]))
    
    return ports    