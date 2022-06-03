#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 18:36:07 2022

@author: eliasmehssatou
"""

# import database
from odbAccess import *

 

filename = 'LHS_data_1-5000.txt'

with open(filename, 'r') as f:
    for sample in f.readlines():
        odb_title = "Job-" + sample.replace('[','').replace(']','').replace(';','').replace('.','p').replace(',','').replace(' ','-').replace('\n','')
        odb_name = odb_title + ".odb"
        print(odb_name)

        # odb_title = 'Job-24p18801625-1p78846425-21p5875-37p935-19p731-8p885e6'
        # odb_name = odb_title + ".odb"
        odb = openOdb(path=odb_name)
        
        
        step1 = odb.steps['Step-1']
        frame = step1.frames[-1] # Last frame in step
        

        sdvs = frame.fieldOutputs['SDV19']
        fieldValues = sdvs.values

        
        outputMAPL1 = open(odb_title + '-STRESSMAPL1.txt','w')
        outputMAPL2 = open(odb_title + '-STRESSMAPL2.txt','w')
        
        
        counter = 0
        counter_L1 = 0
        counter_L2 = 7938
        
        outputMAPL1.write('[')
        outputMAPL2.write('[')
        
        for v in fieldValues:
            # Element, type=M3D4R
            if v.baseElementType == 'M3D4R':
                if counter < 3969:
                    # outputFile.write('Element_M3D4R_L1 = ' + str(v.elementLabel) + '; shear angle [°] = ' + str(v.data) + '\n') 
                    outputMAPL1.write(str(round(v.data,2)))
                    counter_L1 += 1
                
                    if counter_L1%63 == 0:
                        outputMAPL1.write('];')
                        if counter_L1 < 3969:
                            outputMAPL1.write('\n[')
                        else:
                            counter_L1 = 0
                    else:
                        outputMAPL1.write(', ')
                        
                        
                if 7938 <= counter < 11907:
                    # outputFile.write('Element_M3D4R_L2 = ' + str(v.elementLabel) + '; shear angle [°] = ' + str(v.data) + '\n') 
                    outputMAPL2.write(str(round(v.data,2)))
                    counter_L2 += 1
                    if counter_L2%63 == 0:
                        outputMAPL2.write('];')
                        if counter_L2 < 11907:
                            outputMAPL2.write('\n[')
                        else:
                            counter_L2 = 0
                    else:
                        outputMAPL2.write(', ')
            counter += 1
            
        outputMAPL1.close()
        outputMAPL2.close()
        
        

