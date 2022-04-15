#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 14:27:54 2022

@author: eliasmehssatou
"""

import numpy as np

filename = 'LHS_data.txt'

#data = np.loadtxt(filename, unpack = True, delimiter=';')
#print(data)

data_ref = np.array([[7.7375, 35.3625, 36.8125, 33.375, 46.86300000000001, 14.155],[7.7375, 35.3625, 36.8125, 33.375, 46.86300000000001, 14.155]])

print(data_ref)

#data = np.array([])
filename = 'LHS_data.txt'
counter = 0
with open(filename, 'r') as f:
    for line in f.readlines():
        l = line.strip().replace('[','').replace(']','').replace(';','').split(',')
        l_float = [float(d) for d in l]
        if counter == 0:
            data = np.array([l_float])
        if counter >= 1:
            a = np.array([l_float])
            data = np.concatenate((data, a), axis=0)
        counter += 1

for i in range(len(data[:,0])):
    print(data[i,0])