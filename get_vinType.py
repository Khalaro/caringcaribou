
import re
#import pandas as pd
import os
import subprocess



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

     
    
def get_vinType( VIN_CODE_LIST , headers, modes, pids, protocols, formulas): 
    for index,vin_code_slug in enumerate(VIN_CODE_LIST):
        output_filename= VIN_CODE_LIST[index] + ".txt" #"vin_output.txt"
        #if os.path.isfile( output_filename):
        #    os.system("rm  output_filename")
        if not os.path.isfile( output_filename):
            command=("autopi cmd.run 'autopi obd.query VIN_READ header=%s mode=%s pid=%s force=True protocol=%s formula=%s ' >> %s " %( headers[index], modes[index], pids[index], protocols[index], formulas[index], output_filename  ))
            os.system(command)
            #print(command)
        with open(output_filename) as file:
            file_contents = file.read()
        if (  (my_dict['VIN_VALUE'].search(file_contents)) is not None):
            output_vin = (my_dict['VIN_VALUE'].findall(file_contents))[0][0:]
            if validate_vin(output_vin):
                #print( output_vin +"  Protocol: "+protocols[index]+"     Vincodelist: "+VIN_CODE_LIST[index])
                #if os.path.isfile( output_filename):
                #    os.system("rm  "+output_filename)
                return VIN_CODE_LIST[index]
     #       else:
     #           if os.path.isfile( output_filename):
     #               os.system("rm  "+output_filename)
     #  else:
     #      if os.path.isfile( output_filename):
    #return "NOT FOUND","NOT FOUND"
    #command = "rm ./go_build_testproject_go_linux_arm_getslug" 
    #os.system(command)
    #if not os.path.isfile( "go_build_testproject_go_linux_arm_getslug"):
    #command = "wget https://raw.githubusercontent.com/Khalaro/caringcaribou/master/go_build_testproject_go_linux_arm_getslug" 
    #os.system(command)
    #command = "chmod 777 ./go_build_testproject_go_linux_arm_getslug" 
    #os.system(command)
    
    #command=("autopi cmd.run 'autopi cmd.run VIN_READ header=%s mode=%s pid=%s force=True protocol=%s formula=%s ' >> %s " %( headers[index], modes[index], pids[index], protocols[index], formulas[index], output_filename  ))
           
    #command="autopi cmd.run './go_build_testproject_go_linux_arm_getslug >> $timeout=200 vin_slug_bin.txt '"
    command="autopi cmd.run 'autopi cmd.run ./go_build_testproject_go_linux_arm_getslug' >  vin_slug_bin.txt"
    #command=("autopi cmd.run 'cmd.run ./go_build_testproject_go_linux_arm_getslug' >> %s $timeout=200 " %( "vin_slug_bin.txt",  ))
    print(command)
    os.system(command)
    #print(command)
    with open("./vin_slug_bin.txt") as file:
        file_contents = file.read()
            #os.system("rm  "+output_filename)
    return file_contents


def main():    
    formulas= ["""'messages[0].data[3:20]'""",
        """'messages[0].data[3:20]'""",
        """'messages[0].data[3:20]'""",
        #"""'int(messages[0].data[4:],16)/10'""",
        #"""'int(messages[0].data[4:],16)/10'""",
        #"""'int(messages[0].data[4:],16)/10'""",
        """'messages[0].data[3:20]'""",
        """'messages[0].data[3:20]'""",
        """'messages[0].data[4:21]'""",
        """'messages[0].data[4:21]'""",
        """'messages[0].data[3:20]'""",
        """'messages[0].data[4:21]'""",
        """'messages[0].data[2:19]'""",
        """'messages[0].data[2:19]'""",
        """'messages[0].data[5:22]'""",
        """'messages[0].data[5:22]'""",
        """'messages[0].data[2:19]'""",
        """'messages[0].data[5:22]'"""]

    protocols=['6',			  
        '6',		  
        '7',		  
        #'6',		  
        #'6',		  
        #'7',		  
        '6',		  
        '6',		  
        '6',		  
        '6',		  
        '7',		  
        '7',		  
        '6',		  
        '6',		  
        '6',		  
        '6',		  
        '7',		  
        '7']

    headers=['7DF',			  
        '7e0',		  
        '18DB33F1',		  
        #'7DF',		  
        #'7DF',		  
        #'18DB33F1',		  
        '7df',		  
        '7e0',		  
        '7df',		  
        '7e0',		  
        '18DB33F1',		  
        '18DB33F1',		  
        '7df',		  
        '7e0',		  
        '7df',		  
        '7e0',		  
        '18DB33F1',		  
        '18DB33F1']

    pids=['02',  
        '02',  
        '02',  
       #'A6',  
       #'A6',  
       #'A6',  
        'F190',
        'F190',
        'F190',
        'F190',
        'F190',
        'F190',
        'F190',
        'F190',
        'F190',
        'F190',
        'F190',
        'F190']

    modes=['09',
        '09',
        '09',
        #'01',
        #'01',
        #'01',
        '22', 
        '22', 
        '22', 
        '22', 
        '22', 
        '22', 
        '22', 
        '22', 
        '22', 
        '22', 
        '22', 
        '22'] 

    VIN_CODE_LIST= ['vin_7DF_09_02',     
        'vin_7e0_09_02',     
        'vin_18DB33F1_09_02',
        #'vin_7DF_A6',        
        #'vin_7e0_A6',        
        #'vin_18DB33F1_A6',   
        'vin_7DF_UDS_3',     
        'vin_7e0_UDS_3',     
        'vin_7DF_UDS_4',     
        'vin_7e0_UDS_4',     
        'vin_18DB33F1_UDS_3',
        'vin_18DB33F1_UDS_4',
        'vin_7DF_UDS_2',     
        'vin_7e0_UDS_2',     
        'vin_7DF_UDS_5',     
        'vin_7e0_UDS_2',     
        'vin_18DB33F1_UDS_2',
        'vin_18DB33F1_UDS_5']
    found_vin_slug = get_vinType( VIN_CODE_LIST , headers, modes, pids, protocols, formulas)
    print(found_vin_slug)

        
main()
