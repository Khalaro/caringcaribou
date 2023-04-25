
import re
#import pandas as pd
import os
import subprocess




def main():        
  command = "rm ./get_vinType.py" 
  os.system(command)
  command = "wget https://raw.githubusercontent.com/Khalaro/caringcaribou/master/get_vinType.py" 
  os.system(command)    
  command = "rm ./go_build_testproject_go_linux_arm_getslug" 
  os.system(command)
  command = "wget https://raw.githubusercontent.com/Khalaro/caringcaribou/master/go_build_testproject_go_linux_arm_getslug" 
  os.system(command)
  command = "chmod 777 ./go_build_testproject_go_linux_arm_getslug" 
  os.system(command)

        
main()
