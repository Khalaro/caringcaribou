
import re
#import pandas as pd
import os
import subprocess




my_dict = {
    'CLIENT': re.compile(r'\b0x(?P<CLIENT>[0-9A-Fa-f]+)\b \| 0x[0-9A-Fa-f]+\b \|'),
    'SERVER': re.compile(r'\b0x[0-9A-Fa-f]+\b \| 0x(?P<SERVER>[0-9A-Fa-f]+)\b \|'),
}



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
    os.system("python cc.py uds services 0x720 0x728 > services_out.txt")
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
