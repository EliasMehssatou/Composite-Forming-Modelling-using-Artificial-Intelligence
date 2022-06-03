#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 22:46:50 2022

@author: eliasmehssatou
"""

import fileinput
import shutil


filename = 'LHS_data_1-5000.txt'
amount_of_samples = 101

sh_launcher = open('sh_launcher.sh','w')
abq = "find -name '*.abq' -and -not -name '*-en.abq' -type f -exec rm '{}' \;\n"
com = "find -name '*.com' -and -not -name '*-en.com' -type f -exec rm '{}' \;\n"
mdl = "find -name '*.mdl' -and -not -name '*-en.mdl' -type f -exec rm '{}' \;\n"
msg = "find -name '*.msg' -and -not -name '*-en.msg' -type f -exec rm '{}' \;\n"
pac = "find -name '*.pac' -and -not -name '*-en.pac' -type f -exec rm '{}' \;\n"
prt = "find -name '*.prt' -and -not -name '*-en.prt' -type f -exec rm '{}' \;\n"
res = "find -name '*.res' -and -not -name '*-en.res' -type f -exec rm '{}' \;\n"
sel = "find -name '*.sel' -and -not -name '*-en.sel' -type f -exec rm '{}' \;\n"
stt = "find -name '*.stt' -and -not -name '*-en.stt' -type f -exec rm '{}' \;\n"

counter = 0
with open(filename, 'r') as f:
    for sample in f.readlines():
        Job_name = "Job-" + sample.replace('[','').replace(']','').replace(';','').replace('.','p').replace(',','').replace(' ','-').replace('\n','').replace('e6','') 
  
# Job_name = "Job-15p475-70p725-36p8125-33p375-48p263-15p555e62018test2"
        filename_inp = Job_name + ".inp"

# TEXT TO REPLACE FOR SHELL L1
# ** Section: shell_L1
# *Shell Section, elset=L1_sh, material=L1
# 0.14, 5
# *End Part

        orientation_L1 = 45.
        orientation_L2 = -45.
        
        
        modif_shellL1_1 = "** Section: shell_L1"
        modif_shellL1_2 = "*Shell General Section, elset=L1_sh, density=1.E-9,poisson=0.3, User, PROPERTIES=22, VARIABLES=50"
        modif_shellL1_3 = "0.14, \n 229.76,  2682.6, 2.0297, 2.2976, 26.826, 0.020297, 2.2976, 26.826 \n 0.020297,  0., 0., 0.,  0.001, 0.23715, 0.011636,    0.0010042   \n -2.8346,  -4.1531, 10.,    10.,   " + str(orientation_L1) + ", 5  \n *TRANSVERSE SHEAR STIFFNESS \n 1., 1., 0.0000"
        
        modif_shellL2_1 = "** Section: shell_L2"
        modif_shellL2_2 = "*Shell General Section, elset=L2_sh, density=1.E-9,poisson=0.3, User, PROPERTIES=22, VARIABLES=50"
        modif_shellL2_3 = "0.14, \n 229.76,  2682.6, 2.0297, 2.2976, 26.826, 0.020297, 2.2976, 26.826 \n 0.020297,  0., 0., 0.,  0.001, 0.23715, 0.011636,    0.0010042   \n -2.8346,  -4.1531, 10.,    10.,   " + str(orientation_L2) + ", 5  \n *TRANSVERSE SHEAR STIFFNESS \n 1., 1., 0.0000"
        
        counter_L1 = 0
        counter_L2 = 0
          
        with fileinput.FileInput(filename_inp,inplace = True) as f:
            for line in f:
                
                # Shell L1
                if counter_L1 == 2:
                    print(modif_shellL1_3, end ='\n')
                    counter_L1 = 0
                elif counter_L1 == 1:
                    print(modif_shellL1_2, end ='\n')
                    counter_L1 = 2
                elif "** Section: shell_L1" in line:
                    print(modif_shellL1_1, end ='\n')
                    counter_L1 = 1
                    
                # Shell L2
                elif counter_L2 == 2:
                    print(modif_shellL2_3, end ='\n')
                    counter_L2 = 0
                elif counter_L2 == 1:
                    print(modif_shellL2_2, end ='\n')
                    counter_L2 = 2
                elif "** Section: shell_L2" in line:
                    print(modif_shellL2_1, end ='\n')
                    counter_L2 = 1
                    
                # Material orientation
                elif " -1.7805,  -0.887,     10.,     10.,      0." in line: 
                    print(" -1.7805,  -0.887,     10.,     10.,      " + str(orientation_L1), end ='\n')
                elif " -1.7805,  -0.887,     10.,     10.,     90." in line: 
                    print(" -1.7805,  -0.887,     10.,     10.,     " + str(orientation_L2), end ='\n')
                    
                else:
                    print(line, end ='')
                
                
        filename_sh = Job_name + ".sh"
        shutil.copyfile('Job_reference.sh', filename_sh)
        with fileinput.FileInput(filename_sh,inplace = True) as f:
            for line in f:
                if "Job-1" in line:
                    print(line.replace("Job-1",Job_name), end ='')
                else:
                    print(line, end ='')
        
        
        
        sh_launcher.writelines("sh " + filename_sh + ';\n')
        sh_launcher.writelines(abq)
        sh_launcher.writelines(com)
        sh_launcher.writelines(mdl)
        sh_launcher.writelines(msg)
        sh_launcher.writelines(pac)
        sh_launcher.writelines(prt)
        sh_launcher.writelines(res)
        sh_launcher.writelines(sel)
        sh_launcher.writelines(stt)
        
             
sh_launcher.close()   
        
     

            
            
            
            
            