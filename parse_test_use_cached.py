
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
    def is_valid_pair(self):
        if ( (int(self.client_address, base=16)+8) == int(self.server_address, base=16) ):
            return True
        else:
            return False
    server_address = None
    client_address = None
    services_list = [] # class service_code_name_pair
    pid_list =[] # class pid_value_pair

    

def main():

#    with open('discoveryoutput.txt') as file:
#        file_contents = file.read()
        #print(file_contents)
        #return file_contents
    #subprocess.call("python cc.py uds services 0x720 0x728")
    # cmd.run 'python cc.py uds discovery -min 0x000 -max 0xfff'
    #os.system("python cc.py uds discovery -min 0x600 -max 0x7ff >  discovery_output.txt")
    if not os.path.isfile('discovery_output.txt'):
        os.system("python cc.py uds discovery -min 0x000 -max 0xfff >  discovery_output.txt")
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
        if CS_pair.is_valid_pair(): 
            if CS_pair not in myarray:
                myarray.append(CS_pair)
    print('discovery_output: \n clients     servers \n')
    for CS_pair in myarray:        
        print(CS_pair.client_address+'      '+CS_pair.server_address)
        
        

    for CS_pair in myarray:        
        print("python cc.py uds services 0x%s 0x%s > services_out_%s_%s.txt"%(CS_pair.client_address, CS_pair.server_address, CS_pair.client_address, CS_pair.server_address) )

        #Enable for live scanning
        
        if not os.path.isfile('services_out_%s_%s.txt'%( CS_pair.client_address, CS_pair.server_address)):
            os.system("python cc.py uds services 0x%s 0x%s > services_out_%s_%s.txt"%(CS_pair.client_address, CS_pair.server_address, CS_pair.client_address, CS_pair.server_address) )
        #with open( 'services_out_backup.txt'  )as file:
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
        
    service_out_file = open( 'services_out.txt', 'w' )
    for Client_Server_pair in myarray:
        print('Client ID :  '+Client_Server_pair.client_address+'     Server ID :  '+ Client_Server_pair.server_address)
        service_out_file.write('Client ID :  '+Client_Server_pair.client_address+'     Server ID :  '+ Client_Server_pair.server_address)
        for service_code_pair in Client_Server_pair.services_list:
            print(service_code_pair.service_code+'  :  '+ service_code_pair.service_name )
            service_out_file.write(service_code_pair.service_code+'  :  '+ service_code_pair.service_name)
    service_out_file.close()            
        
        
    for CS_pair in myarray:      
        #python cc.py uds dump_dids --min_did 0x6180 --max_did 0x6190  0x720 0x728        
        #os.system("python cc.py uds dump_dids --min_did 0x6180 --max_did 0x6190 0x%s 0x%s > pids_out_%s_%s.txt"%(CS_pair.client_address, CS_pair.server_address, CS_pair.client_address, CS_pair.server_address) )
        #os.system("python cc.py uds dump_dids --min_did 0x0000 --max_did 0xffff 0x%s 0x%s > pids_out_%s_%s.txt"%(CS_pair.client_address, CS_pair.server_address, CS_pair.client_address, CS_pair.server_address) )
        print( 'PID scanning for  ' +  CS_pair.client_address +'    '+ CS_pair.server_address )
        hex_values = [  '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' ]
        for val in hex_values:
            print("python cc.py uds dump_dids --min_did 0x%s000 --max_did 0x%sfff 0x%s 0x%s > pids_out_%s_%s_%s000_%sfff.txt"%(val, val, CS_pair.client_address, CS_pair.server_address, CS_pair.client_address, CS_pair.server_address,val,val ) )
            if not os.path.isfile('pids_out_%s_%s_%s000_%sfff.txt'%(CS_pair.client_address, CS_pair.server_address,val,val )):
                os.system("python cc.py uds dump_dids --min_did 0x%s000 --max_did 0x%sfff 0x%s 0x%s > pids_out_%s_%s_%s000_%sfff.txt"%(val, val, CS_pair.client_address, CS_pair.server_address, CS_pair.client_address, CS_pair.server_address,val,val ) )


        for val in hex_values:
            with open( "pids_out_%s_%s_%s000_%sfff.txt"%( CS_pair.client_address, CS_pair.server_address,val,val ) )as file:
            #with open("pids_out_%s_%s.txt"%(CS_pair.client_address, CS_pair.server_address ) )as file:    
            #with open( 'dup_dids_6000_7000_720_728.txt' )as file:
                pid_file_contents = file.read()        
            pid_codes = my_dict['PID'].findall(pid_file_contents)
            pid_data_values = my_dict['VALUE'].findall(pid_file_contents)                       
            for index,pid in enumerate(pid_codes):
                pid_row = pid_value_pair()
                pid_row.pid_code=pid_codes[index]
                pid_row.data_value=pid_data_values[index]
                print( 'PIDS: '+pid_codes[index] + '        '+   pid_data_values[index]    )
                CS_pair.pid_list.append(pid_row)
                

#        with open( 'dup_dids_6000_7000_720_728.txt' )as file:
#        #with open("pids_out_%s_%s.txt"%(CS_pair.client_address, CS_pair.server_address ) )as file:    
#            pid_file_contents = file.read()        
#        pid_codes = my_dict['PID'].findall(pid_file_contents)
#        pid_data_values = my_dict['VALUE'].findall(pid_file_contents)


    
#    for CS_pair in myarray:
#        print('server_address   |   client_address \n')
#        print(CS_pair.server_address + '  |   '+  CS_pair.client_address+'\n')
#        print('PIDS   |   VALUES \n')
#        for pid in CS_pair.pid_list:
#            print(pid.pid_code + ' : ' + pid.data_value + '\n')
        
    
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
