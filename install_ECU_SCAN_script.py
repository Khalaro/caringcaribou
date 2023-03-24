
import re
#import pandas as pd
import os
import subprocess




def main():
    os.system('pip install python-can')
    os.system('wget https://github.com/CaringCaribou/caringcaribou/archive/refs/heads/master.zip')
    os.system('unzip master.zip -d caribou')
    os.system('cp -r caribou/caringcaribou-master/tool/* ./' )
    os.system('echo "[default] \n interface = socketcan \n channel = can0" > /root/.canrc')
    os.system('echo "[default] \n interface = socketcan \n channel = can0" > /.canrc')
    os.system('rm parse_test_pid_only_on_demand_use_cached.py' )
    os.system('wget https://raw.githubusercontent.com/Khalaro/caringcaribou/master/parse_test_pid_only_on_demand_use_cached.py')
    #os.system('python parse_test_pid_only_on_demand_use_cached.py')

  
    
main()
