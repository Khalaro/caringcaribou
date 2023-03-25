
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
    'ECU_NAME_KEY': re.compile(r'\bvalue: "(?P<ECU_NAME>.+)"'),
    'GENERIC_VALUE_KEY': re.compile(r'\bvalue: "(?P<GENERIC_VALUE_KEY>.+)"'),
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
        
    def check_UDS_DIDS(self, UDS_DIDS_LIST , UDS_DIDS_DESCRIPTIONS): #UDS DIDS to query
        #print(self.server_address)
        #print(("ecu_name_%s_out.txt"%(self.server_address,)))
        for index,standard_did in enumerate(UDS_DIDS_LIST):
            if not os.path.isfile("UDS_DID_out_%s_DID_%s.txt"%(self.server_address , standard_did)):
                #os.system("autopi obd.query UDS_DID_QUERY header="'%s'" mode="'22'" pid="'%s'" force=True protocol=6 formula='messages[0].data' >> UDS_DID_out_%s_DID_%s.txt"%(self.server_address , standard_did, self.server_address , standard_did))
                os.system("autopi obd.query UDS_DID_QUERY header='%s' mode=22 pid='%s' force=True protocol=6 formula='messages[0].data[0:]' >> UDS_DID_out_%s_DID_%s.txt"%(self.server_address , standard_did, self.server_address , standard_did))
            with open('UDS_DID_out_%s_DID_%s.txt'%(self.server_address ,standard_did)) as file:
                uds_did_file_contents = file.read()
            if (  (my_dict['GENERIC_VALUE_KEY'].search(uds_did_file_contents)) is not None):
                self.UDS_DID_response[standard_did] = (my_dict['GENERIC_VALUE_KEY'].findall(uds_did_file_contents))[0][1:]
                print( 'ECU :'+self.server_address +'   DID:'+standard_did+'  Value: '+self.UDS_DID_response[standard_did]+'    Description: '+UDS_DIDS_DESCRIPTIONS[index])
            else:
                self.UDS_DID_response[standard_did] = "Not Available"
                print( 'ECU :'+self.server_address +'   DID:'+standard_did+'  Value: '+self.UDS_DID_response[standard_did]+'    Description: '+UDS_DIDS_DESCRIPTIONS[index])
            
            
    def check_ecu_name(self): 
        #print(self.server_address)
        #print(("ecu_name_%s_out.txt"%(self.server_address,)))
        if not os.path.isfile("ecu_name_%s_out.txt"%(self.server_address,)):
            os.system("autopi obd.query test_pid00 mode=09 pid='0A' header='%s' formula='messages[0].data[3:]' protocol=6 force=true >> ecu_name_%s_out.txt"%(self.server_address,self.server_address))
        with open('ecu_name_%s_out.txt'%(self.server_address,)) as file:
            ecu_name_file_contents = file.read()
        if (  (my_dict['ECU_NAME_KEY'].search(ecu_name_file_contents)) is not None):
            self.ecu_name=(my_dict['ECU_NAME_KEY'].findall(ecu_name_file_contents))[0]
        else:
            self.ecu_name = "Not Available"
        
    def check_service_mode9(self): # return a list of 32 bools representing support for pids 1-32 on this ECU
        if not os.path.isfile("pid_indices_%s_out.txt"%(self.server_address,)):
            print("autopi obd.query test_pid00 mode=09 pid=0 header=%s formula='bin(bytes_to_int(messages[0].data))' protocol=6 force=true >> pid_indices_%s_out.txt"%(self.server_address,self.server_address))
            #print("autopi obd.query test_pid00 mode=09 pid=0 header=%s formula='bin(bytes_to_int(messages[0].data))' protocol=6 force=true >> pid_indices_%s_out.txt"%(self.server_address,self.server_address))
            os.system("autopi obd.query test_pid00 mode=09 pid=0 header=%s formula='bin(bytes_to_int(messages[0].data))' protocol=6 force=true >> pid_indices_%s_out.txt"%(self.server_address,self.server_address))
        with open("pid_indices_%_out.txt"%(self.server_address,)) as file:
            pid_indices_file_contents = file.read()
        pid_supported_list = [True,]  #we create index 0 so later indices correlate to pids
        pid_index_binary_string=((my_dict['PID_KEYv2'].findall(pid_indices_file_contents))[0])[17:49]
        print(pid_index_binary_string)
        for binary_digit in pid_index_binary_string:
            if binary_digit=='1':
                pid_supported_list.append(True)
            else:
                pid_supported_list.append(False)
        return pid_supported_list

    def get_pid_indices(self): # return a list of 32 bools representing support for pids 1-32 on this ECU
        if not os.path.isfile('pid_indices_out.txt'):
            os.system("obd.query test_pid00 mode=09 pid="'0'" header="'7df'" formula='bin(bytes_to_int(messages[0].data))' protocol=6 force=true   >> pid_indices_out.txt")
        with open('pid_indices_out.txt') as file:
            pid_indices_file_contents = file.read()
        pid_index_binary_string=(my_dict['PID_KEY'].findall(pid_indices_file_contents))[0]
        pid_supported_list = [True,]  #we create index 0 so later indices correlate to pids
        pid_index_binary_string=((my_dict['PID_KEYv2'].findall(pid_indices_file_contents))[0])[2:34]
        print(pid_index_binary_string)
        for binary_digit in pid_index_binary_string:
            if binary_digit=='1':
                pid_supported_list.append(True)
            else:
                pid_supported_list.append(False)
        print(pid_supported_list)
        for index, inx in enumerate(pid_supported_list):
            #print(inx)
            if inx:
                print('supported PID:')
                print(hex(index))
            else:
                print('UNsupported PID:')
                print(hex(index))

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
    ecu_name = None
    services_list = [] # class service_code_name_pair
    pid_list =[] # class pid_value_pair
    UDS_DID_response = {} # map [string UDS_DUD] 
    


def main():
    
    UDS_DID_list =['F180', 'F181', 'F182', 'F183', 'F184', 'F185', 'F186', 'F187', 'F188', 'F189', 'F18A', 'F18B', 'F18C', 'F18D', 'F18E', 'F190', 'F191', 'F192', 'F193', 'F194', 'F195', 'F196', 'F197', 'F198', 'F199', 'F19A', 'F19B', 'F19C', 'F19D', 'F19E', 'F19F']
    UDS_DID_description =['bootSoftwareIdentificationDataIdentifier',
                        'applicationSoftwareIdentificationDataIdentifier',
                        'applicationDataIdentificationDataIdentifier',
                        'bootSoftwareIdentificationDataIdentifier',
                        'applicationSoftwareFingerprintDataIdentifier',
                        'applicationDataFingerprintDataIdentifier',
                        'activeDiagnosticSessionDataIdentifier',
                        'vehicleManufacturerSparePartNumberDataIdentifier',
                        'vehicleManufacturerECUSoftwareNumberDataIdentifier',
                        'vehicleManufacturerECUSoftwareVersionNumberDataIdentifier',
                        'systemSupplierIdentifierDataIdentifier',
                        'ECUManufacturingDateDataIdentifier',
                        'ECUSerialNumberDataIdentifier',
                        'supportedFunctionalUnitsDataIdentifier',
                        'vehicleManufacturerKitAssemblyPartNumberDataIdentifier',
                        'VINDataIdentifier',
                        'vehicleManufacturerECUHardwareNumberDataIdentifier',
                        'systemSupplierECUHardwareNumberDataIdentifier',
                        'systemSupplierECUHardwareVersionNumberDataIdentifier',
                        'systemSupplierECUSoftwareNumberDataIdentifier',
                        'systemSupplierECUSoftwareVersionNumberDataIdentifier',
                        'exhaustRegulationOrTypeApprovalNumberDataIdentifier',
                        'systemNameOrEngineTypeDataIdentifier',
                        'repairShopCodeOrTesterSerialNumberDataIdentifier',
                        'programmingDateDataIdentifier',
                        'calibrationRepairShopCodeOrCalibrationEquipmentSerialNumberDataIdentifier',
                        'calibrationDateDataIdentifier',
                        'calibrationEquipmentSoftwareNumberDataIdentifier',
                        'ECUInstallationDateDataIdentifier',
                        'ODXFileDataIdentifier',
                        'entityDataIdentifier']
    if not os.path.isfile('discovery_output.txt'):
        os.system("python cc.py uds discovery -min 0x700 -max 0x800 >  discovery_output.txt")
    with open('discovery_output.txt') as file:
        discovery_file_contents = file.read()
    clients = my_dict['CLIENT'].findall(discovery_file_contents)
    servers = my_dict['SERVER'].findall(discovery_file_contents)
    myarray = []  
    myarray.append(client_server_pair('7D7', '7DF')) # add the Generic ECU reference
    for index,value in enumerate(clients):    
        CS_pair = client_server_pair(clients[index], servers[index])
        if CS_pair.is_valid_pair(): 
            if CS_pair not in myarray:
                myarray.append(CS_pair)
    print('discovery_output: \n clients     servers \n')
    for CS_pair in myarray:        
        print(CS_pair.client_address+'      '+CS_pair.server_address)

    for CS_pair in myarray:        
        #print("python cc.py uds services 0x%s 0x%s > services_out_%s_%s.txt"%(CS_pair.client_address, CS_pair.server_address, CS_pair.client_address, CS_pair.server_address) )
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
        Client_Server_pair.check_ecu_name()
        Client_Server_pair.check_UDS_DIDS(UDS_DID_list, UDS_DID_description)
        print('\n\n\n\n\Client ID :  '+Client_Server_pair.client_address+'     Server ID :  '+ Client_Server_pair.server_address + '  ECU NAME:  ' + Client_Server_pair.ecu_name)
        service_out_file.write('Client ID :  '+Client_Server_pair.client_address+'     Server ID :  '+ Client_Server_pair.server_address)
        for service_code_pair in Client_Server_pair.services_list:
            print(service_code_pair.service_code+'  :  '+ service_code_pair.service_name +'    \n' )
            service_out_file.write(service_code_pair.service_code+'  :  '+ service_code_pair.service_name)
    service_out_file.close()            


main()
