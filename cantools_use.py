
import re
#import pandas as pd
import os
import datetime
import subprocess
import can
import time
#from can import Message
#from can import Filter



my_dict = {
    'Other_VALUE': re.compile(r'0x[0-9A-Fa-f]+ (?P<VALUE>[0-9A-Fa-f]+)?'), 
    #'VIN_VALUE': re.compile(r'value: (?P<VIN_VALUE>[A-Za-z0-9]+)'),
    'VIN_VALUE': re.compile(r'\bvalue: (?P<VIN_VALUE>[A-Za-z0-9]+)'),
    'KEY': re.compile(r'.'),
	}

class CustomListener(can.Listener):
    def __init__(self):
        self.messages = []
    
    def on_message_received(self, msg):
        if True:  #msg.arbitration_id in [0x215, 0x073, 0x201]:
            self.messages.append(msg)
            print("Received message with arbitration ID {}: {}".format(msg.arbitration_id, msg.data))

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


def test_read(): 
    filters = [{"can_id": 0x215, "can_mask": 0x2FF, "extended": False}, 
			{"can_id": 0x073, "can_mask": 0x0FF, "extended": False}, 
			{"can_id": 0x201, "can_mask": 0x2FF, "extended": False}]
    can_bus = can.interface.Bus('can0', bustype='socketcan', can_filters=filters)
    #can_bus = can.ThreadSafeBus(channel='can0', bustype='socketcan', can_filters=filters)
    message = can_bus.recv()
    print('OUT 1:')
    print(message)
    time.sleep(10.0) 
    message = can_bus.recv()
    print('OUT 2:')
    print(message)

    start_time = datetime.datetime.now()
    while True:
	message = can_bus.recv()
        print('OUT 3:')
        print(message)
	current_time = datetime.datetime.now()
	if (current_time - start_time).total_seconds() >= 10:
		break
    #if message.arbitration_id == 0x215:
    #    citreon_vin[0:3]= message.data
    #if message.arbitration_id == 0x073:
    #    citreon_vin[3:9]= message.data
    #if message.arbitration_id == 0x201:
    #    citreon_vin[9:17]= message.data


def test_read_and_translate(): 
    filters = [{"can_id": 0x215, "can_mask": 0x2FF, "extended": False}, 
			{"can_id": 0x073, "can_mask": 0x0FF, "extended": False}, 
			{"can_id": 0x201, "can_mask": 0x2FF, "extended": False}]
    can_bus = can.interface.Bus('can0', bustype='socketcan', can_filters=filters)
    #can_bus = can.ThreadSafeBus(channel='can0', bustype='socketcan', can_filters=filters)
    segA=False
    segB=False
    segC=False
    start_time = datetime.datetime.now()
    citreon_vin=[]
    while True:
	message = can_bus.recv()
	if message.arbitration_id == 0x215:
		citreon_vin[0:3]= message.data
		#print(message.data)
		segA=True
	if message.arbitration_id == 0x073:
		citreon_vin[3:9]= message.data
		#print(message.data)
		segB=True
	if message.arbitration_id == 0x201:
		citreon_vin[9:17]= message.data
		#print(message.data)
		segC=True
	current_time = datetime.datetime.now()
	if (segA and segB and segC):
		print("ALL CIITROEN VIN VALUES FOUND!!!!!!")
		print(citreon_vin)
		break
	if (current_time - start_time).total_seconds() >= 10:
		break
    print('OUT 3:')
    if (segA and segB and segC):
		print(citreon_vin)
    #citreon_vin_string = ''
    #for chrctr in citreon_vin:
	#citreon_vin_string+=char(chrctr)
    #print(citreon_vin_string)

def test_read_v2(): 
    filters = [{"can_id": 0x215, "can_mask": 0x7FF, "extended": False}, 
			{"can_id": 0x073, "can_mask": 0x7FF, "extended": False}, 
			{"can_id": 0x201, "can_mask": 0x7FF, "extended": False}]
    #can_bus = can.interface.Bus('can0', bustype='socketcan')
    can_bus = can.interface.Bus('can0', bustype='socketcan', can_filters=filters)
    #can_bus = can.ThreadSafeBus('can0', bustype='socketcan')
    #can_bus = can.ThreadSafeBus(channel='can0', bustype='socketcan', can_filters=filters)
    #data = example_message.encode({'Temperature': 250.1, 'AverageRadius': 3.2, 'Enable': 1})
    #message = can.Message(arbitration_id=example_message.frame_id, data=data)
    #can_bus.send(message)
    #canddd=444
    citreon_vin=[]
    ascii_bytes=[]
    start_time = datetime.datetime.now()
    #message = can_bus.recv()
    #db.decode_message(message.arbitration_id, message.data)

    
    messagelist=[]
    message1 = can.Message(data=[1, 2, 3, 4, 5, 6, 7, 8],arbitration_id=533) #533 = 0x215
    message2 = can.Message(data=[1, 2, 3, 4, 5, 6, 7, 8],arbitration_id=0x073)
    message3 = can.Message(data=[1, 2, 3, 4, 5, 6, 7, 8],arbitration_id=0x201) 
    #messagelist.append(message1)
    #messagelist.append(message2)
    #messagelist.append(message3)
    #message = can_bus.recv()
    
    mylistener=CustomListener()
    notifier = can.Notifier(can_bus, [mylistener,], timeout=8.0)

    while True:
	current_time = datetime.datetime.now()
	if (current_time - start_time).total_seconds() >= 10:
	    break    
    #can_bus.recv()
    for msg in mylistener.messages:
	print(msg)
    #can_bus.recv()
    #mylistener.on_message_received(message1)
    #mylistener.on_message_received(message2)
    #mylistener.on_message_received(message3)
    #notifier.add_listener(mylistener)
    
    #for message in messagelist:
    #    if message.arbitration_id == 0x215:
    #        citreon_vin[0:3]= message.data
    #    if message.arbitration_id == 0x073:
    #        citreon_vin[3:9]= message.data
    #    if message.arbitration_id == 0x201:
    #        citreon_vin[9:17]= message.data
	
    if False:	
	    if len(mylistener.messages) > 0:
		print(len(mylistener.messages))
	    while True:
		current_time = datetime.datetime.now()
		if (current_time - start_time).total_seconds() >= 10:
		    break    
	    for message in mylistener.messages:
		if message.arbitration_id == 0x215:
		    citreon_vin[0:3]= message.data
		if message.arbitration_id == 0x073:
		    citreon_vin[3:9]= message.data
		if message.arbitration_id == 0x201:
		    citreon_vin[9:17]= message.data

	    print(citreon_vin)
	
    #notifier.stop()
    #while False:
    #    message = Message(data=[1, 2, 3, 4, 5, 6, 7, 8],arbitration_id=533) #533 = 0x215
    #    #message = can_bus.recv()
    #    if message.arbitration_id == 0x215:
    #        citreon_vin[0:3]= message.data
    #    if message.arbitration_id == 0x073:
    #        citreon_vin[3:9]= message.data
    #    if message.arbitration_id == 0x201:
    #        citreon_vin[9:17]= message.data
    #    #for indx,val in enumerate(citreon_vin[0:3]):
    #    #    val = message.data[indx]
    #    #for indx,val in enumerate(citreon_vin[3:9]):
    #    #    val = message.data[indx]
    #    #for indx,val in enumerate(citreon_vin[9:17]):
    #    #    val = message.data[indx]
    #    #citreon_vin[0:3]= message.data
    #    #citreon_vin[3:9]= message.data
    #    #citreon_vin[9:17]= message.data
    #    print(citreon_vin)
    #    #ascii_bytes=[]
    #    #for i,val in enumerate(citreon_vin):
    #    #    ascii_bytes.append(bytes(val).decode("ASCII"))
    #    #    
    #    #print( ascii_bytes )
    #    current_time = datetime.datetime.now()
    #    if (current_time - start_time).total_seconds() >= 10:
    #        break
    
def main():  
    if True:
	test_read_v2()
	#test_read_and_translate()
	#else:
	#    if True: 
	#	test_read()
	#    else:
	#	test_read_v2()
        
main()
