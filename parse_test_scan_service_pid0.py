
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
    'PID_KEYv2': re.compile(r'\b0b[0-1]+\b ?'),
    'KEY': re.compile(r'.'),
}


def check_service_mode9(): # return a list of 32 bools representing support for pids 1-32 on this ECU
    if not os.path.isfile('pid_indices_out.txt'):
        os.system("autopi obd.query test_pid00 mode=09 pid="'0'" header="'7df'" formula='bin(bytes_to_int(messages[0].data))' protocol=6 force=true   >> pid_indices_out.txt")
    with open('pid_indices_out.txt') as file:
        pid_indices_file_contents = file.read()
    pid_supported_list = [True,]  #we create index 0 so later indices correlate to pids
    pid_index_binary_string=((my_dict['PID_KEYv2'].findall(pid_indices_file_contents))[0])[17:49]
    print(pid_index_binary_string)
    for binary_digit in pid_index_binary_string:
        if binary_digit=='1':
            pid_supported_list.append(True)
        else:
            pid_supported_list.append(False)
    print(pid_supported_list)
    for index, inx in enumerate(pid_supported_list):
        if inx:
            print('supported PID:')
            print(hex(index))


def main():
    service_key=check_service_mode9()
  
    
main()
