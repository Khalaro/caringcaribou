
import re
#import pandas as pd
import os
import datetime
import subprocess
import can



my_dict = {
    'Other_VALUE': re.compile(r'0x[0-9A-Fa-f]+ (?P<VALUE>[0-9A-Fa-f]+)?'), 
    #'VIN_VALUE': re.compile(r'value: (?P<VIN_VALUE>[A-Za-z0-9]+)'),
    'VIN_VALUE': re.compile(r'\bvalue: (?P<VIN_VALUE>[A-Za-z0-9]+)'),
    'KEY': re.compile(r'.'),
}


def validate_vin(vinsample): #string
    # We should check the string for special characters before attempting to send to nshta
    if len(vinsample)==17:
        return True
    else:
        return False

     
    
def get_vin_and_protocol( VIN_CODE_LIST , headers, modes, pids, protocols, formulas): 
    for index,vin_code_slug in enumerate(VIN_CODE_LIST):
        output_filename= VIN_CODE_LIST[index] + ".txt" #"vin_output.txt"
        #if os.path.isfile( output_filename):
        #    os.system("rm  output_filename")
        if not os.path.isfile( output_filename):
            command=("autopi cmd.run 'autopi obd.query VIN_READ header=%s mode=%s pid=%s force=True protocol=%s formula=%s ' >> %s " %( headers[index], modes[index], pids[index], protocols[index], formulas[index], output_filename  ))
            os.system(command)
            print(command)
        with open(output_filename) as file:
            file_contents = file.read()
        if (  (my_dict['VIN_VALUE'].search(file_contents)) is not None):
            output_vin = (my_dict['VIN_VALUE'].findall(file_contents))[0][0:]
            if validate_vin(output_vin):
                print( output_vin +"  Protocol: "+protocols[index]+"     Vincodelist: "+VIN_CODE_LIST[index])
                #if os.path.isfile( output_filename):
                #    os.system("rm  "+output_filename)
                return output_vin, protocols[index]
     #       else:
     #           if os.path.isfile( output_filename):
     #               os.system("rm  "+output_filename)
     #  else:
     #      if os.path.isfile( output_filename):
    return "NOT FOUND","NOT FOUND"
                #os.system("rm  "+output_filename)


def main():    
    can_bus = can.interface.Bus('can0', bustype='socketcan')
    #data = example_message.encode({'Temperature': 250.1, 'AverageRadius': 3.2, 'Enable': 1})
    #message = can.Message(arbitration_id=example_message.frame_id, data=data)
    #can_bus.send(message)
    #canddd=444
    citreon_vin=[]
    ascii_bytes=[]
    start_time = datetime.datetime.now()
    message = can_bus.recv()
    #db.decode_message(message.arbitration_id, message.data)
    while True:
        message = can_bus.recv()
        if message.arbitration_id == 0x215:
            citreon_vin[0:8]= message.data
        if message.arbitration_id == 0x073:
            citreon_vin[8:16]= message.data
        if message.arbitration_id == 0x201:
            citreon_vin[16:24]= message.data[0:8]
        print(citreon_vin)
        for i,val in enumerate(citreon_vin):
            ascii_bytes[i] = (bytes(val).decode("ASCII"))
            
        print( ascii_bytes )
        current_time = datetime.datetime.now()
        if (current_time - start_time).total_seconds() >= 10:
            break
    
        
main()
