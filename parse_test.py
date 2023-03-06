
import re
#import pandas as pd
import os
import subprocess




my_dict = {
    'CLIENT': re.compile(r'\b0x(?P<CLIENT>[0-9A-Fa-f]+)\b \| 0x[0-9A-Fa-f]+\b \|'),
    'SERVER': re.compile(r'\b0x[0-9A-Fa-f]+\b \| 0x(?P<SERVER>[0-9A-Fa-f]+)\b \|'),
}

class service_code_name_pair:
    def __eq__(self, other):
        if ((self.service_code == other.service_code) and (self.service_name == other.service_name)):
            return True
        else:
            return False
    service_code = None
    service_name = None
    
class client_server_pair:
    def __eq__(self, other):
        if ((self.server_address == other.server_address) and (self.client_address == other.client_address)):
            return True
        else:
            return False
    server_address = None
    client_address = None
    services_list = []

def main():

    my_dict = {
        'CLIENT': re.compile(r'\b0x(?P<CLIENT>[0-9A-Fa-f]+)\b \| 0x[0-9A-Fa-f]+\b \|'),
        'SERVER': re.compile(r'\b0x[0-9A-Fa-f]+\b \| 0x(?P<SERVER>[0-9A-Fa-f]+)\b \|'),
        'SERVICE_NAME': re.compile(r'Supported service 0x[0-9A-Fa-f]+: (?P<SERVICE_NAME>[^\\\n]+) ?'),
        'SERVICE_CODE': re.compile(r'Supported service (?P<SERVICE_CODE>0x[0-9A-Fa-f]+): [^\\\n]+ ?'),
        'KEY': re.compile(r'.'),
    }
#    with open('discoveryoutput.txt') as file:
#        file_contents = file.read()
        #print(file_contents)
        #return file_contents
    #subprocess.call("python cc.py uds services 0x720 0x728")
    # cmd.run 'python cc.py uds discovery -min 0x000 -max 0xfff'
    #os.system("python cc.py uds discovery -min 0x600 -max 0x7ff >  discovery_output.txt")
    #os.system("python cc.py uds discovery -min 0x000 -max 0xfff >  discovery_output.txt")
    #subprocess.call('ls', '-l')
    with open('discovery_output.txt') as file:
        discovery_file_contents = file.read()
    clients = my_dict['CLIENT'].findall(discovery_file_contents)
    servers = my_dict['SERVER'].findall(discovery_file_contents)
    myarray = []
    for index,value in enumerate(clients):    
        CS_pair = client_server_pair()
        CS_pair.client_address = clients[index]
        CS_pair.server_address = servers[index]
        if CS_pair not in myarray:
            myarray.append(CS_pair)
    print('discovery_output: \n clients     servers \n')
    for CS_pair in myarray:        
        print(CS_pair.client_address+'      '+CS_pair.server_address)
        
        
    
    for CS_pair in myarray:        
        #subprocess.call("python cc.py uds services 0x%s 0x%s > services_out.txt"%(CS_pair.client_address, CS_pair.server_address) )
        print("python cc.py uds services 0x%s 0x%s > services_out.txt"%(CS_pair.client_address, CS_pair.server_address) )
#    with open('discoveryoutput.txt') as file:
#        file_contents = file.read()
        #print(file_contents)
        #return file_contents
        
    #subprocess.call("python cc.py uds services 0x720 0x728 > services_out.txt")
    #subprocess.call("python cc.py uds services 0x720 0x728 > services_out.txt")
    #subprocess.call('ls', '-l')
    with open('services_out.txt') as file:
        services_file_contents = file.read()
#    clients = my_dict['CLIENT'].findall(file_contents)
#    servers = my_dict['SERVER'].findall(file_contents)
    service_names = my_dict['SERVICE_NAME'].findall(services_file_contents)
    service_codes = my_dict['SERVICE_CODE'].findall(services_file_contents)
#    print('clients \n')
#    for x in clients:
#        print(x)
#    print('servers \n')
#    for x in servers:
#        print(x)
    print('service_names \n')
    for x in service_names:
        print(x)
    print('service_codes \n')
    for x in service_codes:
        print(x)
        
    #os.system("python cc.py uds services 0x7e0 0x7e8 > services_out.txt")
    #subprocess.call('ls', '-l')
    with open('services_out.txt') as file:
        services_file_contents = file.read()
#    clients = my_dict['CLIENT'].findall(file_contents)
#    servers = my_dict['SERVER'].findall(file_contents)
    service_names = my_dict['SERVICE_NAME'].findall(services_file_contents)
    service_codes = my_dict['SERVICE_CODE'].findall(services_file_contents)
#    print('clients \n')
#    for x in clients:
#        print(x)
#    print('servers \n')
#    for x in servers:
#        print(x)
    print('service_names \n')
    for x in service_names:
        print(x)
    print('service_codes \n')
    for x in service_codes:
        print(x)




def _parse_line(line):
    """
    Do a regex search against all defined regexes and
    return the key and match result of the first matching regex

    """

    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    # if there are no matches
    return None, None
    
    
main()
