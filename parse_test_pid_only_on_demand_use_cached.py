
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
    'VALUE': re.compile(r'0x[0-9A-Fa-f]+ (?P<VALUE>[0-9A-Fa-f]+)?'), 
    'PID_KEY': re.compile(r'\bvalue: 7e8[0-9A-Fa-f]{2}([0-9A-Fa-f]+)\b ?'),
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
    def __init__(self, client_id, server_id):
        self.server_address = server_id
        self.client_address = client_id
    def __eq__(self, other):
        if ( self.values_match(other.client_address, other.server_address)):
            return True
        else:
            return False
    def values_match(self, client_id, server_id):  #(string client_id, string server_id)
        if (    int(self.client_address, base=16) == int(client_id, base=16)  and  int(self.server_address, base=16) == int(server_id, base=16)   ):
            return True
        else:
            return False
    def is_valid_pair(self):
        if ( (int(self.client_address, base=16)+8) == int(self.server_address, base=16) ):
            return True
        else:
            return False
    def get_pid_indices(self): # return a list of 16 bools representing support for pids 1-32 on this ECU
        if not os.path.isfile('pid_indices_out.txt'):
            os.system("obd.query test_pid01 mode=01 pid=01 header=\"'%'\" bytes=4  protocol=6 force=true  >> pid_indices_out.txt"%(self.client_address))
        with open('pid_indices_out.txt') as file:
        pid_indices_file_contents = file.read()
        pid_index_hex_string=(my_dict['PID_KEY'].findall(pid_indices_file_contents))[0]
        pid_supported_list = [False,] #there is no pid zero, but we create inxex 0 so later inicies correlate to pids
        for hex_digit in pid_index_hex_string[0:8]:
            hex_digit_binary_value=bin(int(hex_digit,16))
            four_digit_string=(str(hex_digit_binary_value))[2:6]
            missing_zeros = 4-len(four_digit_string)
            for i in range(missing_zeros):
                four_digit_string = '0' + four_digit_string
            #print(four_digit_string)
            for bit in four_digit_string:
                if bit=='0':
                    pid_supported_list.append(False)
                else:
                    pid_supported_list.append(True)
        #print(pid_supported_list)
        return pid_supported_list
        #for index, inx in enumerate(pid_supported_list):
            #print(inx)
        #    if inx:
        #        print('supported PID:')
        #        print(hex(index))
        
    def query_pids(self, min_pid, max_pid): # ex.  self.query_pid("6182","6184")
        print( 'PID scanning for  ' +  self.client_address +'    '+ self.server_address )
        print("python cc.py uds dump_dids --min_did 0x%s --max_did 0x%s 0x%s 0x%s > pids_out_%s_%s_%s_%s.txt"%(min_pid,max_pid, self.client_address, self.server_address, self.client_address, self.server_address,min_pid,max_pid ) )
        if not os.path.isfile('pids_out_%s_%s_%s_%s.txt'%(self.client_address, self.server_address, min_pid, max_pid )):
            os.system("python cc.py uds dump_dids --min_did 0x%s --max_did 0x%s 0x%s 0x%s > pids_out_%s_%s_%s_%s.txt"%(min_pid,max_pid, self.client_address, self.server_address, self.client_address, self.server_address,min_pid,max_pid ) )
        with open( "pids_out_%s_%s_%s_%s.txt"%( self.client_address, self.server_address,min_pid,max_pid ) )as file:
            pid_file_contents = file.read()        
        pid_codes = my_dict['PID'].findall(pid_file_contents)
        pid_data_values = my_dict['VALUE'].findall(pid_file_contents)                       
        for index,pid in enumerate(pid_codes):
            pid_row = pid_value_pair()
            pid_row.pid_code=pid_codes[index]
            pid_row.data_value=pid_data_values[index]
            print( 'PIDS: '+pid_codes[index] + '        '+   pid_data_values[index]    )
            self.pid_list.append(pid_row)
    server_address = None
    client_address = None
    services_list = [] # class service_code_name_pair
    pid_list =[] # class pid_value_pair

    

def main():
    if not os.path.isfile('discovery_output.txt'):
        os.system("python cc.py uds discovery -min 0x000 -max 0xfff >  discovery_output.txt")
    with open('discovery_output.txt') as file:
        discovery_file_contents = file.read()
    clients = my_dict['CLIENT'].findall(discovery_file_contents)
    servers = my_dict['SERVER'].findall(discovery_file_contents)
    myarray = []
    for index,value in enumerate(clients):    
        CS_pair = client_server_pair(clients[index], servers[index])
        if CS_pair.is_valid_pair(): 
            if CS_pair not in myarray:
                myarray.append(CS_pair)
    print('discovery_output: \n clients     servers \n')
    for CS_pair in myarray:        
        print(CS_pair.client_address+'      '+CS_pair.server_address)

    for CS_pair in myarray:        
        print("python cc.py uds services 0x%s 0x%s > services_out_%s_%s.txt"%(CS_pair.client_address, CS_pair.server_address, CS_pair.client_address, CS_pair.server_address) )
        if not os.path.isfile('services_out_%s_%s.txt'%( CS_pair.client_address, CS_pair.server_address)):
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
        
    service_out_file = open( 'services_out.txt', 'w' )
    for Client_Server_pair in myarray:
        print('Client ID :  '+Client_Server_pair.client_address+'     Server ID :  '+ Client_Server_pair.server_address)
        service_out_file.write('Client ID :  '+Client_Server_pair.client_address+'     Server ID :  '+ Client_Server_pair.server_address)
        for service_code_pair in Client_Server_pair.services_list:
            print(service_code_pair.service_code+'  :  '+ service_code_pair.service_name )
            service_out_file.write(service_code_pair.service_code+'  :  '+ service_code_pair.service_name)
    service_out_file.close()            
        
    
main()
