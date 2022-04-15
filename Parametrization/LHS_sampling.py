#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 23:42:33 2021

@author: eliasmehssatou
"""

import numpy as np
import matplotlib.pyplot as plt
from smt.sampling_methods import LHS



lx = [0.001, 50.0]
ly = [0.001, 50.0]
alpha = [0.0, 60.0]
h = [20.0, 70.0]
rtop = [2.0, 70.0]
rbot = [2.0, 70.0]

composite_dimension = 190


xlimits = np.array([lx, ly, h, alpha, rtop, rbot])
sampling = LHS(xlimits=xlimits)

LHS_total = 20000  # Total number of LHS samples, should be high enough to surpass the filtering (±5*LHS_amount)
x = sampling(LHS_total)
#print(x.shape)

plt.plot(x[:, 0], x[:, 4], "o")
plt.xlabel("x")
plt.ylabel("y")
plt.show()


LHS_amount = 3  # Number of LHS samples that will be added in database (must be < LHS_total)
LHS_samples = []
i = 0
while len(LHS_samples) < LHS_amount:
    # print(i)
    # x axis (minor) must be smaller than y axis (major)
    if x[i, 0] < x[i, 1]:
        i += 1
        continue
    # height condition if alpha = 0 
    if x[i, 2] == 0 and x[i, 3] < x[i, 4] + x[i, 5] + 2.8:
        i += 1
        continue
    # height condition if alpha != 0 
    if x[i, 2] != 0 and x[i, 3] < (x[i, 4] + x[i, 5] + 2.8)*(1-np.sin(x[i, 2]*np.pi/180)):
        i += 1
        continue 
    # perimeter of mould must be smaller than dimension of composite
    if (x[i, 4]/(np.tan((x[i, 2]*np.pi/180+np.pi/2)/2)) + x[i, 3]*np.tan(x[i, 2]*np.pi/180) + x[i, 5]/(np.tan((x[i, 2]*np.pi/180+np.pi/2)/2)) + x[i, 3])*2 + x[i, 1] > composite_dimension:
        i += 1
        continue
    
    LHS_samples.append([round(x[i,0],8),round(x[i,1],8),round(x[i,2],8),round(x[i,3],8),round(x[i,4],8),round(x[i,5],8)])
    i += 1
    
    if i == LHS_total:
        print("Entire sampling space searched; either increase LHS_total or reduce LHS_amount")
        break


file = open('LHS_data.txt','w')
i = 0
for items in LHS_samples:
    i += 1
    if i == len(LHS_samples):
        file.writelines(str(items)+'\n')
    else: 
        file.writelines(str(items)+';\n')
file.close()


