#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 17:22:00 2021

@author: eliasmehssatou
"""


# https://stackoverflow.com/questions/22959698/distance-from-given-point-to-given-ellipse
# https://github.com/0xfaded/ellipse_demo/issues/1

import sys
sys.modules[__name__].__dict__.clear()

import sys
import math 
import numpy as np
from PIL import Image


def ellips_point_distance(semi_major, semi_minor, p):  
    px = abs(p[0])
    py = abs(p[1])

    tx = 0.707
    ty = 0.707

    a = semi_major
    b = semi_minor

    for x in range(0, 3):
        x = a * tx
        y = b * ty

        ex = (a*a - b*b) * tx**3 / a
        ey = (b*b - a*a) * ty**3 / b

        rx = x - ex
        ry = y - ey

        qx = px - ex
        qy = py - ey

        r = math.hypot(ry, rx)
        q = math.hypot(qy, qx)

        tx = min(1, max(0, (qx * r / q + ex) / a))
        ty = min(1, max(0, (qy * r / q + ey) / b))
        t = math.hypot(ty, tx)
        tx /= t 
        ty /= t 

    return (math.copysign(a * tx, p[0]), math.copysign(b * ty, p[1]))


#data = [7, 2, 20, 50, 46.86300000000001, 20]



f = open("LHS_data.txt", "r")
LHS_data = np.matrix(f.read())

for i in range (2):#len(LHS_data)):
    
    
    ly = LHS_data[i,0]
    lx = LHS_data[i,1]
    alpha = LHS_data[i,2]
    alpha_rad = alpha*np.pi/180
    h = LHS_data[i,3]
    rtop = LHS_data[i,4]
    rbot = LHS_data[i,5]
    
    if LHS_data[i,0] < LHS_data[i,1]:
        print("Height map generation aborted; ly < lx")
        sys.exit()
        
    if LHS_data[i,2] == 0 and LHS_data[i,3] < LHS_data[i,4] + LHS_data[i,5] + 2.8:
        print("Height map generation aborted; alpha = 0 height constraint not respected")
        sys.exit()
    elif LHS_data[i,2] != 0 and LHS_data[i,3] < (LHS_data[i,4] + LHS_data[i,5] + 2.8)*(1-np.sin(LHS_data[i,2]*np.pi/180)):
        print("Height map generation aborted; alpha != 0 height constraint not respected")
        sys.exit()
    
    resolution  = 200
    X = np.linspace(0,100,num = resolution)
    Y = np.linspace(0,100,num = resolution)
    
    heightmap = np.ones([len(X),len(Y)])
    
    for x in range (len(X)):
        for y in range(len(Y)):
            if x**2/(lx/2)**2 + y**2/(ly/2)**2 <= 1:
                heightmap[len(X)-x-1,y] = h
            else:
                if alpha != 0:
                    closest_point = ellips_point_distance(lx/2, ly/2, [x,y])
                    d = math.dist(closest_point,[x,y])
                    if d <= rtop*np.cos(alpha_rad):
                        heightmap[len(X)-x-1,y] = h - (rtop - np.sqrt(rtop**2 - d**2))
                    elif d <= rtop/np.tan((alpha_rad + np.pi/2)/2) + h*np.tan(alpha_rad) + rbot/np.tan((alpha_rad + np.pi/2)/2) - rbot*np.cos(alpha_rad):
                        heightmap[len(X)-x-1,y] = (rtop/np.tan((alpha_rad + np.pi/2)/2) + h*np.tan(alpha_rad) - d)/np.tan(alpha_rad)
                    elif d <= rtop/np.tan((alpha_rad + np.pi/2)/2) + h*np.tan(alpha_rad) + rbot/np.tan((alpha_rad + np.pi/2)/2):
                        heightmap[len(X)-x-1,y] = rbot - np.sqrt(rbot**2 - (rtop/np.tan((alpha_rad + np.pi/2)/2) + h*np.tan(alpha_rad) + rbot/np.tan((alpha_rad + np.pi/2)/2)- d)**2)
                    elif d > rtop/np.tan((alpha_rad + np.pi/2)/2) + h*np.tan(alpha_rad) + rbot/np.tan((alpha_rad + np.pi/2)/2):
                        heightmap[len(X)-x-1,y] = 0
                else:
                    closest_point = ellips_point_distance(lx/2, ly/2, [x,y])
                    d = math.dist(closest_point,[x,y])
                    if d <= rtop*np.cos(alpha_rad):
                        heightmap[len(X)-x-1,y] = h - (rtop - np.sqrt(rtop**2 - d**2))
                    elif d <= rtop+rbot:
                        heightmap[len(X)-x-1,y] = rbot - np.sqrt(rbot**2 - (rbot-d)**2)
                    elif d > rtop+rbot:
                        heightmap[len(X)-x-1,y] = 0
    
    
    Q1 = np.asanyarray(heightmap)
    Q2 = np.flipud(Q1)
    Q12 = np.concatenate((Q1, Q2), axis=0)
    Q12copy = Q12[:,:]
    Q34 = np.fliplr(Q12)
    total_heightmap = np.concatenate((Q34, Q12), axis=1)
    
    total_heightmap_grayscale = total_heightmap*255/70
    
    file = open(str(lx)+"; "+str(ly)+"; "+str(alpha)+"; "+str(h)+"; "+str(rtop)+"; "+str(rbot)+"; GEOM.txt",'w')
    for items in total_heightmap_grayscale:
        file.writelines(str(items)+',\n')
    file.close()
    
    # # CREATE GRAYSCALE IMAGE
    # # Add space for colorbar 
    # cbar = np.ones([50,len(X)*2])*255
    # grayscale = np.concatenate((total_heightmap_grayscale,cbar), axis=0)
    
    
    # im = Image.fromarray(grayscale)
    # im = im.convert("L")
    # im.save(str(lx)+"; "+str(ly)+"; "+str(alpha)+"; "+str(h)+"; "+str(rtop)+"; "+str(rbot)+"; GEOM.png")
    # im.show()
    
    
    
    




























