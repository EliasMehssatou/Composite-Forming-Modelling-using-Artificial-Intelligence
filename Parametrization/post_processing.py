#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 16:45:38 2022

@author: eliasmehssatou
"""



import math 
import numpy as np
import sys 
import fileinput 

from PIL import Image




# filename = 'LHS_data.txt'

# with open(filename, 'r') as f:
#     for sample in f.readlines():
#         shearmap_title = "Job-" + sample.replace('[','').replace(']','').replace(';','').replace('.','p').replace(',','').replace(' ','-')
#         shearmap_name = shearmap_title + "-SHEARMAPL1.txt"


shearmap_temp = 'Job-41p18767625-40p38769225-57p6125-22p125-9p939-18p847-SHEARMAPL1.txt'
shearmap_title = "Job-" + shearmap_temp.replace('[','').replace(']','').replace(';','').replace('.','p').replace(',','').replace(' ','-')
shearmap_name = shearmap_title + "-SHEARMAPL1.txt"


counter = 0
with open(shearmap_name, 'r') as f:
    for line in f.readlines():
        l = line.strip().replace('[','').replace(']','').replace(';','').split(',')
        l_float = [float(d) for d in l]
        if counter == 0:
            data = np.array([l_float])
        if counter >= 1:
            a = np.array([l_float])
            data = np.concatenate((data, a), axis=0)
        counter += 1
        
shearmap_grayscale = (data + abs(np.amin(data)))*255/50


im = Image.fromarray(shearmap_grayscale)
im = im.convert("L")
im.save(shearmap_title + "-SHEARMAPL1.png")
im.show()