
import re
#import pandas as pd
import os
import subprocess



my_dict = {
    'CLIENT': re.compile(r'\b0x(?P<CLIENT>[0-9A-Fa-f]+)\b \| 0x[0-9A-Fa-f]+\b \|'),
    'SERVER': re.compile(r'\b0x[0-9A-Fa-f]+\b \| 0x(?P<SERVER>[0-9A-Fa-f]+)\b \|'),
    'SERVICE_NAME': re.compile(r'Supported service 0x[0-9A-Fa-f]+: (?P<SERVICE_NAME>[^\\\n]+) ?'),
    'SERVICE_CODE': re.compile(r'Supported service (?P<SERVICE_CODE>0x[0-9A-Fa-f]+): [^\\\n]+ ?'),
    'PID': re.compile(r'0x(?P<PID>[0-9A-Fa-f]+) [0-9A-Fa-f]+?'),
    'VALUE': re.compile(r'0x[0-9A-Fa-f]+ (?P<VALUE>[0-9A-Fa-f]+)?'),  #    (0x[0-9A-Fa-f]+) ([0-9A-Fa-f]+)?
    'KEY': re.compile(r'.'),
}

class pid_value_pair:
    def __eq__(self, other):
        if ((self.pid_code == other.pid_code) and (self.data_value == other.data_value)):
            return True
        else:
            return False
    pid_code = None
    data_value = None


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
    pid_list =[]

    
    
def pidtest():  
    myarray=[]
    myarray.append(client_server_pair())
    myarray[0].client_address = '00000720'
    myarray[0].server_address = '00000728'
    #pid_list=[]
    #services_list =[]
    print("python cc.py uds services 0x%s 0x%s > services_out_%s_%s.txt"%('00000720', '00000728', '00000720', '00000728') )
    os.system("python cc.py uds services 0x%s 0x%s > services_out_%s_%s.txt"%('00000720', '00000728', '00000720', '00000728') )
    with open("services_out_%s_%s.txt"%('00000720', '00000728' ) )as file:
        services_file_contents = file.read()
    service_codes = my_dict['SERVICE_CODE'].findall(services_file_contents)
    service_names = my_dict['SERVICE_NAME'].findall(services_file_contents)

    for index,value in enumerate(service_codes):
        service_code_name_row = service_code_name_pair()
        service_code_name_row.service_code = service_codes[index]
        service_code_name_row.service_name = service_names[index]
        if service_code_name_row not in myarray[0].services_list:
            myarray[0].services_list.append(service_code_name_row)
    #if server address is 8 greater than client address, then we will scan the pair for pids
    if(  (int('00000720', base=16)+8) == int('00000728', base=16)  ):
        #python cc.py uds dump_dids --min_did 0x6180 --max_did 0x6190  0x720 0x728        
        #os.system("python cc.py uds dump_dids --min_did 0x0000 --max_did 0xffff 0x%s 0x%s > pids_out_%s_%s.txt"%(CS_pair.client_address, CS_pair.server_address, CS_pair.client_address, CS_pair.server_address) )
        print("python cc.py uds dump_dids --min_did 0x6180 --max_did 0x6190 0x%s 0x%s > pids_out_%s_%s.txt"%('00000720', '00000728', '00000720', '00000728') )
        #os.system("python cc.py uds dump_dids --min_did 0x6180 --max_did 0x6190 0x%s 0x%s > pids_out_%s_%s.txt"%(CS_pair.client_address, CS_pair.server_address, CS_pair.client_address, CS_pair.server_address) )
        with open("pids_out_%s_%s.txt"%('00000720', '00000728' ) )as file:
            pid_file_contents = file.read()        
        pid_codes = my_dict['PID'].findall(pid_file_contents)
        pid_data_values = my_dict['VALUE'].findall(pid_file_contents)

        for index,pid in enumerate(pid_codes):
            pid_row = pid_value_pair()
            pid_row.pid_code=pid_codes[index]
            pid_row.data_value=pid_data_values[index]
            myarray[0].pid_list.append(pid_row)

    for CS_pair in myarray:
        print('server_address   |   client_address \n')
        print(CS_pair.server_address + '  |   '+  CS_pair.client_address+'\n')
        print('PIDS   |   VALUES \n')
        for pid in CS_pair.pid_list:
            print(pid.pid_code + ' : ' + pid.data_value + '\n')
    
    
def main():

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
        print("python cc.py uds services 0x%s 0x%s > services_out_%s_%s.txt"%(CS_pair.client_address, CS_pair.server_address, CS_pair.client_address, CS_pair.server_address) )
        os.system("python cc.py uds services 0x%s 0x%s > services_out_%s_%s.txt"%(CS_pair.client_address, CS_pair.server_address, CS_pair.client_address, CS_pair.server_address) )
        with open("services_out_%s_%s.txt"%(CS_pair.client_address, CS_pair.server_address ) )as file:
            services_file_contents = file.read()
        service_codes = my_dict['SERVICE_CODE'].findall(services_file_contents)
        service_names = my_dict['SERVICE_NAME'].findall(services_file_contents)
        
        for index,value in enumerate(service_codes):
            service_code_name_row = service_code_name_pair()
            service_code_name_row.service_code = service_codes[index]
            service_code_name_row.service_name = service_names[index]
            if service_code_name_row not in CS_pair.services_list:
                CS_pair.services_list.append(service_code_name_row)
        #if server address is 8 greater than client address, then we will scan the pair for pids
        if( (int(CS_pair.client_address, base=16)+8) == int(CS_pair.server_address, base=16)   ): #(int(CS_pair.client_address, base=16)+8) == int(CS_pair.server_address, base=16) 
            #print(CS_pair.server_address +'    '+CS_pair.client_address)
            #print(   (int(CS_pair.server_address, base=16)+8) == int(CS_pair.client_address, base=16) )
            #print('/n')
            #print(   (int(CS_pair.server_address, base=16)+8) )
            #print('/n')
            #print( int(CS_pair.client_address, base=16) )
            #print('/n')
            #python cc.py uds dump_dids --min_did 0x6180 --max_did 0x6190  0x720 0x728        
            #os.system("python cc.py uds dump_dids --min_did 0x0000 --max_did 0xffff 0x%s 0x%s > pids_out_%s_%s.txt"%(CS_pair.client_address, CS_pair.server_address, CS_pair.client_address, CS_pair.server_address) )
            #os.system("python cc.py uds dump_dids --min_did 0x6180 --max_did 0x6190 0x%s 0x%s > pids_out_%s_%s.txt"%(CS_pair.client_address, CS_pair.server_address, CS_pair.client_address, CS_pair.server_address) )
            os.system("python cc.py uds dump_dids --min_did 0x0000 --max_did 0xffff 0x%s 0x%s > pids_out_%s_%s.txt"%(CS_pair.client_address, CS_pair.server_address, CS_pair.client_address, CS_pair.server_address) )
            with open("pids_out_%s_%s.txt"%(CS_pair.client_address, CS_pair.server_address ) )as file:
                pid_file_contents = file.read()        
            pid_codes = my_dict['PID'].findall(pid_file_contents)
            pid_data_values = my_dict['VALUE'].findall(pid_file_contents)

            for index,pid in enumerate(pid_codes):
                pid_row = pid_value_pair()
                pid_row.pid_code=pid_codes[index]
                pid_row.data_value=pid_data_values[index]
                print( 'PIDS: '+pid_codes[index] + '        '+   pid_data_values[index]    )
                CS_pair.pid_list.append(pid_row)
    
    for CS_pair in myarray:
        print('server_address   |   client_address \n')
        print(CS_pair.server_address + '  |   '+  CS_pair.client_address+'\n')
        print('PIDS   |   VALUES \n')
        for pid in CS_pair.pid_list:
            print(pid.pid_code + ' : ' + pid.data_value + '\n')
        
    #subprocess.call("python cc.py uds services 0x720 0x728 > services_out.txt")
    #subprocess.call("python cc.py uds services 0x720 0x728 > services_out.txt")
    #subprocess.call('ls', '-l')
#    clients = my_dict['CLIENT'].findall(file_contents)
#    servers = my_dict['SERVER'].findall(file_contents)
#    print('clients \n')
#    for x in clients:
#        print(x)
#    print('servers \n')
#    for x in servers:
#        print(x)

    
main()
#pidtest()
