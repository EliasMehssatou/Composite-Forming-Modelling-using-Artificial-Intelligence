# -*- coding: mbcs -*-


import math 
import numpy as np
import sys 
import fileinput 

#session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)
filename = 'LHS_data_1561-1611.txt'
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

#[21.5625, 35.9125, 22.2125, 99.54*(1-math.sin(22.2125*math.pi/180)), 31.325, 68.215] ; Working radiuses
#[7.7375*2, 35.3625*2, 36.8125, 33.375, 46.86300000000001, 14.155] ; Parametrization flagship (figure 4.1)
#[0.01, 0.01, 0.0, 30.0, 62.0, 2] ; Experimental reference
#data = np.array([[0.01, 0.01, 0.0, 30.0, 62.0, 2]])



for i in range(len(data[:,0])):
    from part import *
    from material import *
    from section import *
    from assembly import *
    from step import *
    from interaction import *
    from load import *
    from mesh import *
    from optimization import *
    from job import *
    from sketch import *
    from visualization import *
    from connectorBehavior import *
    
    #print("---------- Start of geometry generation ----------"+'\n')
    ############# PARAMETER INITIALIZATION #############
    lmin = data[i,0] # must be > 0.01 for experimental cases (h<rtop)
    lmax = data[i,1] # must be > 0.01 for experimental cases (h<rtop)
    alpha = data[i,2]
    alpha_rad = alpha*math.pi/180
    h = data[i,3]
    rtop = data[i,4] #59.9999
    rbot = data[i,5]

    #print("lmin = "+ str(lmin) +'\n')
    #print("lmax = "+ str(lmax) +'\n')
    #print("alpha = "+ str(alpha) +'\n')
    #print("h = "+ str(h) +'\n')
    #print("rtop = "+ str(rtop) +'\n')
    #print("rbot = "+ str(rbot) +'\n\n')
    
    #print((rtop/(math.tan((alpha_rad+math.pi/2)/2))+h*math.tan(alpha_rad)+rbot/(math.tan((alpha_rad+math.pi/2)/2))+h)*2 + lmax)
    
    Job_name = "Job-"+str(lmin)+"-"+str(lmax)+"-"+str(alpha)+"-"+str(h)+"-"+str(rtop)+"-"+str(rbot)#+"e6"
    Job_name_corrected = Job_name.replace(".", "p")


    ############# CREATE TOP MOULD #############
    mdb.Model(name='Model-1')

    ############# Sweep #############
    # Create sweep path, top ellips
    mdb.models['Model-'+str(1)].ConstrainedSketch(name='__sweep__', sheetSize=200.0)
    # mdb.models['Model-1'].sketches['__sweep__'].rectangle(point1=(lmin/2, 0.0), 
    #     point2=(0.0, -lmax/2))
    mdb.models['Model-'+str(1)].sketches['__sweep__'].EllipseByCenterPerimeter(
        axisPoint1=(lmin/2, 0.0), axisPoint2=(0.0, -lmax/2), center=(0.0, 0.0))
    mdb.models['Model-'+str(1)].ConstrainedSketch(name='__profile__', sheetSize=200.0, 
        transform=(1.0, 0.0, 0.0, 0.0, 0.0, 1.0, -0.0, -1.0, -0.0, lmin/2, 0.0, 0.0))
        

    # Create construction lines
    mdb.models['Model-'+str(1)].sketches['__profile__'].ConstructionLine(point1=(-100.0, 
        0.0), point2=(100.0, 0.0))
    mdb.models['Model-'+str(1)].sketches['__profile__'].ConstructionLine(point1=(0.0, 
        -100.0), point2=(0.0, 100.0))

    # Create lines
    if h < rtop and alpha == 0.0:
        #print("h < rtop and alpha == 0.0")
        mdb.models['Model-'+str(1)].sketches['__profile__'].Arc3Points(point1=(0.0, 0.0), 
            point2=(rtop*math.cos(math.asin((rtop-h)/rtop)), -h), point3=(rtop*math.cos(math.asin((rtop-h/2)/rtop)), -h/2))

        mdb.models['Model-'+str(1)].sketches['__profile__'].Line(point1=(rtop*math.cos(math.asin((rtop-h)/rtop)), -h), 
            point2=(rtop*math.cos(math.asin((rtop-h)/rtop))+rbot+10, -h))
        mdb.models['Model-'+str(1)].sketches['__profile__'].HorizontalConstraint(
            addUndoState=False, entity=
            mdb.models['Model-'+str(1)].sketches['__profile__'].geometry[5])

        if rbot != 0.0:
            mdb.models['Model-'+str(1)].sketches['__profile__'].FilletByRadius(curve1=
                mdb.models['Model-'+str(1)].sketches['__profile__'].geometry[4], curve2=
                mdb.models['Model-'+str(1)].sketches['__profile__'].geometry[5], nearPoint1=(rtop*math.cos(math.asin((rtop-h/2)/rtop)), -h/2), nearPoint2=(rtop*math.cos(math.asin((rtop-h)/rtop))+rbot/2, -h), radius=rbot)
        mdb.models['Model-'+str(1)].ConstrainedSketch(name='Sketch-1', objectToCopy=
            mdb.models['Model-'+str(1)].sketches['__profile__'])

    else:
        mdb.models['Model-'+str(1)].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(rtop/(math.tan((alpha_rad+math.pi/2)/2)), 0.0))
        mdb.models['Model-'+str(1)].sketches['__profile__'].HorizontalConstraint(
            addUndoState=False, entity=
            mdb.models['Model-'+str(1)].sketches['__profile__'].geometry[4])
        mdb.models['Model-'+str(1)].sketches['__profile__'].ParallelConstraint(addUndoState=
            False, entity1=mdb.models['Model-'+str(1)].sketches['__profile__'].geometry[2], 
            entity2=mdb.models['Model-'+str(1)].sketches['__profile__'].geometry[4])
        mdb.models['Model-'+str(1)].sketches['__profile__'].CoincidentConstraint(
            addUndoState=False, entity1=
            mdb.models['Model-'+str(1)].sketches['__profile__'].vertices[0], entity2=
            mdb.models['Model-'+str(1)].sketches['__profile__'].geometry[2])
        mdb.models['Model-'+str(1)].sketches['__profile__'].CoincidentConstraint(
            addUndoState=False, entity1=
            mdb.models['Model-'+str(1)].sketches['__profile__'].vertices[1], entity2=
            mdb.models['Model-'+str(1)].sketches['__profile__'].geometry[2])
            
        mdb.models['Model-'+str(1)].sketches['__profile__'].Line(point1=(rtop/(math.tan((alpha_rad+math.pi/2)/2)), 
            0.0), point2=(rtop/(math.tan((alpha_rad+math.pi/2)/2))+h*math.tan(alpha_rad), -h))

        mdb.models['Model-'+str(1)].sketches['__profile__'].Line(point1=(rtop/(math.tan((alpha_rad+math.pi/2)/2))+h*math.tan(alpha_rad), -h), 
            point2=(rtop/(math.tan((alpha_rad+math.pi/2)/2))+h*math.tan(alpha_rad)+rbot/(math.tan((alpha_rad+math.pi/2)/2))+11, -h)) 
        mdb.models['Model-'+str(1)].sketches['__profile__'].HorizontalConstraint(
            addUndoState=False, entity=
            mdb.models['Model-'+str(1)].sketches['__profile__'].geometry[6])

        if rtop != 0.0:
            mdb.models['Model-'+str(1)].sketches['__profile__'].FilletByRadius(curve1=
                mdb.models['Model-'+str(1)].sketches['__profile__'].geometry[4], curve2=
                mdb.models['Model-'+str(1)].sketches['__profile__'].geometry[5], nearPoint1=(
                (rtop/(math.tan((alpha_rad+math.pi/2)/2)))/2, 0), nearPoint2=(rtop*math.cos(math.pi/4-alpha_rad/2), -(rtop - rtop*math.sin(math.pi/4-alpha_rad/2))), radius=rtop)
        if rbot != 0.0:
            mdb.models['Model-'+str(1)].sketches['__profile__'].FilletByRadius(curve1=
                mdb.models['Model-'+str(1)].sketches['__profile__'].geometry[5], curve2=
                mdb.models['Model-'+str(1)].sketches['__profile__'].geometry[6], nearPoint1=((rtop/(math.tan((alpha_rad+math.pi/2)/2))+h*math.tan(alpha_rad))*0.75, -h*0.75), nearPoint2=(rtop/(math.tan((alpha_rad+math.pi/2)/2))+h*math.tan(alpha_rad)+(rbot/(math.tan((alpha_rad+math.pi/2)/2))+1)/2, -h), radius=rbot)
        mdb.models['Model-'+str(1)].ConstrainedSketch(name='Sketch-1', objectToCopy=
            mdb.models['Model-'+str(1)].sketches['__profile__'])

    # Perform sweep
    mdb.models['Model-'+str(1)].Part(dimensionality=THREE_D, name='top_rigid', type=
        DEFORMABLE_BODY)
    mdb.models['Model-1'].parts['top_rigid'].BaseShellSweep(path=
        mdb.models['Model-1'].sketches['__sweep__'], sketch=
        mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']
    del mdb.models['Model-1'].sketches['__sweep__']


    # Make top ellipse
    mdb.models['Model-1'].parts['top_rigid'].DatumPlaneByPrincipalPlane(offset=0.0, 
        principalPlane=XYPLANE)
    mdb.models['Model-1'].parts['top_rigid'].DatumAxisByPrincipalAxis(principalAxis=
        XAXIS)
    mdb.models['Model-1'].ConstrainedSketch(gridSpacing=3.2, name='__profile__', 
        sheetSize=128.34, transform=
        mdb.models['Model-1'].parts['top_rigid'].MakeSketchTransform(
        sketchPlane=mdb.models['Model-1'].parts['top_rigid'].datums[2], 
        sketchPlaneSide=SIDE1, 
        sketchUpEdge=mdb.models['Model-1'].parts['top_rigid'].datums[3], 
        sketchOrientation=RIGHT, origin=(0.0, 0.0, 0.0)))
    mdb.models['Model-1'].parts['top_rigid'].projectReferencesOntoSketch(filter=
        COPLANAR_EDGES, sketch=mdb.models['Model-1'].sketches['__profile__'])
    mdb.models['Model-'+str(1)].sketches['__profile__'].EllipseByCenterPerimeter(
        axisPoint1=(0.0, lmin/2), axisPoint2=(-lmax/2, 0.0), center=(0.0, 0.0))
    mdb.models['Model-1'].parts['top_rigid'].Shell(sketch=
        mdb.models['Model-1'].sketches['__profile__'], sketchOrientation=RIGHT, 
        sketchPlane=mdb.models['Model-1'].parts['top_rigid'].datums[2], 
        sketchPlaneSide=SIDE1, sketchUpEdge=
        mdb.models['Model-1'].parts['top_rigid'].datums[3])
    del mdb.models['Model-1'].sketches['__profile__']

    thickness_rigid = 1.0
    thickness_prepreg = 0.14



    ############# CREATE BOTTOM MOULD #############

    t = 1.4
    rtop = rtop + t
    rbot = rbot + t


    ############# Sweep #############
    # Create sweep path, top ellips
    mdb.models['Model-'+str(1)].ConstrainedSketch(name='__sweep__', sheetSize=200.0)
    mdb.models['Model-'+str(1)].sketches['__sweep__'].EllipseByCenterPerimeter(
        axisPoint1=(lmin/2, 0.0), axisPoint2=(0.0, -lmax/2), center=(0.0, 0.0))
    mdb.models['Model-'+str(1)].ConstrainedSketch(name='__profile__', sheetSize=200.0, 
        transform=(1.0, 0.0, 0.0, 0.0, 0.0, 1.0, -0.0, -1.0, -0.0, lmin/2, 0.0, 0.0))
        

    # Create construction lines
    mdb.models['Model-'+str(1)].sketches['__profile__'].ConstructionLine(point1=(-100.0, 
        0.0), point2=(100.0, 0.0))
    mdb.models['Model-'+str(1)].sketches['__profile__'].ConstructionLine(point1=(0.0, 
        -100.0), point2=(0.0, 100.0))

    # Create lines
    if h < rtop and alpha == 0.0:
        #print("h < rtop and alpha == 0.0")
        mdb.models['Model-'+str(1)].sketches['__profile__'].Arc3Points(point1=(0.0, 0.0), 
            point2=(rtop*math.cos(math.asin((rtop-h)/rtop)), -h), point3=(rtop*math.cos(math.asin((rtop-h/2)/rtop)), -h/2))

        mdb.models['Model-'+str(1)].sketches['__profile__'].Line(point1=(rtop*math.cos(math.asin((rtop-h)/rtop)), -h), 
            point2=(rtop*math.cos(math.asin((rtop-h)/rtop))+rbot+10, -h))
        mdb.models['Model-'+str(1)].sketches['__profile__'].HorizontalConstraint(
            addUndoState=False, entity=
            mdb.models['Model-'+str(1)].sketches['__profile__'].geometry[5])
        if rbot != 0.0:
            mdb.models['Model-'+str(1)].sketches['__profile__'].FilletByRadius(curve1=
                mdb.models['Model-'+str(1)].sketches['__profile__'].geometry[4], curve2=
                mdb.models['Model-'+str(1)].sketches['__profile__'].geometry[5], nearPoint1=(rtop*math.cos(math.asin((rtop-h/2)/rtop)), -h/2), nearPoint2=(rtop*math.cos(math.asin((rtop-h)/rtop))+rbot/2, -h), radius=rbot)
        
        
        mdb.models['Model-'+str(1)].ConstrainedSketch(name='Sketch-1', objectToCopy=
            mdb.models['Model-'+str(1)].sketches['__profile__'])

    else:
        mdb.models['Model-'+str(1)].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(rtop/(math.tan((alpha_rad+math.pi/2)/2)), 0.0))
        mdb.models['Model-'+str(1)].sketches['__profile__'].HorizontalConstraint(
            addUndoState=False, entity=
            mdb.models['Model-'+str(1)].sketches['__profile__'].geometry[4])
        mdb.models['Model-'+str(1)].sketches['__profile__'].ParallelConstraint(addUndoState=
            False, entity1=mdb.models['Model-'+str(1)].sketches['__profile__'].geometry[2], 
            entity2=mdb.models['Model-'+str(1)].sketches['__profile__'].geometry[4])
        mdb.models['Model-'+str(1)].sketches['__profile__'].CoincidentConstraint(
            addUndoState=False, entity1=
            mdb.models['Model-'+str(1)].sketches['__profile__'].vertices[0], entity2=
            mdb.models['Model-'+str(1)].sketches['__profile__'].geometry[2])
        mdb.models['Model-'+str(1)].sketches['__profile__'].CoincidentConstraint(
            addUndoState=False, entity1=
            mdb.models['Model-'+str(1)].sketches['__profile__'].vertices[1], entity2=
            mdb.models['Model-'+str(1)].sketches['__profile__'].geometry[2])
            
        mdb.models['Model-'+str(1)].sketches['__profile__'].Line(point1=(rtop/(math.tan((alpha_rad+math.pi/2)/2)), 
            0.0), point2=(rtop/(math.tan((alpha_rad+math.pi/2)/2))+h*math.tan(alpha_rad), -h))

        mdb.models['Model-'+str(1)].sketches['__profile__'].Line(point1=(rtop/(math.tan((alpha_rad+math.pi/2)/2))+h*math.tan(alpha_rad), -h), 
            point2=(rtop/(math.tan((alpha_rad+math.pi/2)/2))+h*math.tan(alpha_rad)+rbot/(math.tan((alpha_rad+math.pi/2)/2))+11, -h)) 
        mdb.models['Model-'+str(1)].sketches['__profile__'].HorizontalConstraint(
            addUndoState=False, entity=
            mdb.models['Model-'+str(1)].sketches['__profile__'].geometry[6])
        if rtop != 0.0:
            mdb.models['Model-'+str(1)].sketches['__profile__'].FilletByRadius(curve1=
                mdb.models['Model-'+str(1)].sketches['__profile__'].geometry[4], curve2=
                mdb.models['Model-'+str(1)].sketches['__profile__'].geometry[5], nearPoint1=(
                (rtop/(math.tan((alpha_rad+math.pi/2)/2)))/2, 0), nearPoint2=(rtop*math.cos(math.pi/4-alpha_rad/2), -(rtop - rtop*math.sin(math.pi/4-alpha_rad/2))), radius=rtop)
        if rbot != 0.0:
            mdb.models['Model-'+str(1)].sketches['__profile__'].FilletByRadius(curve1=
                mdb.models['Model-'+str(1)].sketches['__profile__'].geometry[5], curve2=
                mdb.models['Model-'+str(1)].sketches['__profile__'].geometry[6], nearPoint1=((rtop/(math.tan((alpha_rad+math.pi/2)/2))+h*math.tan(alpha_rad))*0.75, -h*0.75), nearPoint2=(rtop/(math.tan((alpha_rad+math.pi/2)/2))+h*math.tan(alpha_rad)+(rbot/(math.tan((alpha_rad+math.pi/2)/2))+1)/2, -h), radius=rbot)
        
        
        
        mdb.models['Model-'+str(1)].ConstrainedSketch(name='Sketch-1', objectToCopy=
            mdb.models['Model-'+str(1)].sketches['__profile__'])

    # Perform sweep
    mdb.models['Model-'+str(1)].Part(dimensionality=THREE_D, name='bot_rigid', type=
        DEFORMABLE_BODY)
    mdb.models['Model-1'].parts['bot_rigid'].BaseShellSweep(path=
        mdb.models['Model-1'].sketches['__sweep__'], sketch=
        mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']
    del mdb.models['Model-1'].sketches['__sweep__']




    ############# Make bottom ellipse #############
    mdb.models['Model-1'].parts['bot_rigid'].DatumPlaneByPrincipalPlane(offset=0.0, 
        principalPlane=XYPLANE)
    mdb.models['Model-1'].parts['bot_rigid'].DatumAxisByPrincipalAxis(principalAxis=
        XAXIS)
    mdb.models['Model-1'].ConstrainedSketch(gridSpacing=3.2, name='__profile__', 
        sheetSize=128.34, transform=
        mdb.models['Model-1'].parts['bot_rigid'].MakeSketchTransform(
        sketchPlane=mdb.models['Model-1'].parts['bot_rigid'].datums[2], 
        sketchPlaneSide=SIDE1, 
        sketchUpEdge=mdb.models['Model-1'].parts['bot_rigid'].datums[3], 
        sketchOrientation=RIGHT, origin=(0.0, 0.0, 0.0)))
    mdb.models['Model-1'].parts['bot_rigid'].projectReferencesOntoSketch(filter=
        COPLANAR_EDGES, sketch=mdb.models['Model-1'].sketches['__profile__'])
    # mdb.models['Model-'+str(1)].sketches['__profile__'].EllipseByCenterPerimeter(
    #     axisPoint1=(lmin/2, 0.0), axisPoint2=(0.0, -lmax/2), center=(0.0, 0.0))
    mdb.models['Model-'+str(1)].sketches['__profile__'].EllipseByCenterPerimeter(
        axisPoint1=(0.0, lmin/2), axisPoint2=(-lmax/2, 0.0), center=(0.0, 0.0))
    mdb.models['Model-1'].parts['bot_rigid'].Shell(sketch=
        mdb.models['Model-1'].sketches['__profile__'], sketchOrientation=RIGHT, 
        sketchPlane=mdb.models['Model-1'].parts['bot_rigid'].datums[2], 
        sketchPlaneSide=SIDE1, sketchUpEdge=
        mdb.models['Model-1'].parts['bot_rigid'].datums[3])
    del mdb.models['Model-1'].sketches['__profile__']





    ############# CREATE PREPREG PARTS #############

    l = 190.0 # characteristic length of prepreg

    mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
        point2=(l, l))
    mdb.models['Model-1'].Part(dimensionality=THREE_D, name='L1', type=
        DEFORMABLE_BODY)
    mdb.models['Model-1'].parts['L1'].BaseShell(sketch=
        mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']

    mdb.models['Model-1'].Part(name='L2', objectToCopy=
    mdb.models['Model-1'].parts['L1'])




    ############# CREATE MATERIALS #############
    mdb.models['Model-1'].Material(name='L1')
    mdb.models['Model-1'].materials['L1'].Density(table=((1e-09, ), ))
    mdb.models['Model-1'].materials['L1'].Depvar(n=50)
    mdb.models['Model-1'].materials['L1'].UserMaterial(mechanicalConstants=(3.2488, 
        716.561, 1.0001, 0.0812, 17.914, 0.025, 0.0325, 7.1656, 0.01, 0.0, 0.0, 
        0.0, 0.0011, 1.8899, 0.0151, 0.0774, -1.7805, -0.887, 10.0, 10.0, -45.0))
    mdb.models['Model-1'].Material(name='L2', objectToCopy=
        mdb.models['Model-1'].materials['L1'])
    mdb.models['Model-1'].materials['L1'].userMaterial.setValues(
        mechanicalConstants=(3.2488, 716.561, 1.0001, 0.0812, 17.914, 0.025, 
        0.0325, 7.1656, 0.01, 0.0, 0.0, 0.0, 0.0011, 1.8899, 0.0151, 0.0774, 
        -1.7805, -0.887, 10.0, 10.0, 0.0))
    mdb.models['Model-1'].materials['L2'].userMaterial.setValues(
        mechanicalConstants=(3.2488, 716.561, 1.0001, 0.0812, 17.914, 0.025, 
        0.0325, 7.1656, 0.01, 0.0, 0.0, 0.0, 0.0011, 1.8899, 0.0151, 0.0774, 
        -1.7805, -0.887, 10.0, 10.0, 90.0))

    mdb.models['Model-1'].Material(name='rigid')
    mdb.models['Model-1'].materials['rigid'].Density(table=((1e-06, ), ))
    mdb.models['Model-1'].materials['rigid'].Elastic(table=((1000000.0, 0.3), ))




    ############# CREATE SECTION AND ASSIGNMENT TO INSTANCES #############

    # Prepreg
    mdb.models['Model-1'].Part(name='L1_sh', objectToCopy=
        mdb.models['Model-1'].parts['L1'])
    mdb.models['Model-1'].Part(name='L2_sh', objectToCopy=
        mdb.models['Model-1'].parts['L2'])
    mdb.models['Model-1'].MembraneSection(material='L1', name='memb_L1', 
        poissonDefinition=DEFAULT, thickness=thickness_prepreg, thicknessField='', 
        thicknessType=UNIFORM)
    mdb.models['Model-1'].MembraneSection(material='L2', name='memb_L2', 
        poissonDefinition=DEFAULT, thickness=thickness_prepreg, thicknessField='', 
        thicknessType=UNIFORM)
    mdb.models['Model-1'].HomogeneousShellSection(idealization=NO_IDEALIZATION, 
        integrationRule=GAUSS, material='rigid', name='rigid', nodalThicknessField=
        '', numIntPts=3, poissonDefinition=DEFAULT, preIntegrate=OFF, temperature=
        GRADIENT, thickness=thickness_rigid, thicknessField='', thicknessModulus=None, 
        thicknessType=UNIFORM, useDensity=OFF)
    mdb.models['Model-1'].HomogeneousShellSection(idealization=NO_IDEALIZATION, 
        integrationRule=SIMPSON, material='L1', name='shell_L1', 
        nodalThicknessField='', numIntPts=5, poissonDefinition=DEFAULT, 
        preIntegrate=OFF, temperature=GRADIENT, thickness=thickness_prepreg, thicknessField='', 
        thicknessModulus=None, thicknessType=UNIFORM, useDensity=OFF)
    mdb.models['Model-1'].HomogeneousShellSection(idealization=NO_IDEALIZATION, 
        integrationRule=SIMPSON, material='L2', name='shell_L2', 
        nodalThicknessField='', numIntPts=5, poissonDefinition=DEFAULT, 
        preIntegrate=OFF, temperature=GRADIENT, thickness=thickness_prepreg, thicknessField='', 
        thicknessModulus=None, thicknessType=UNIFORM, useDensity=OFF)
    mdb.models['Model-1'].parts['L1'].Set(faces=
        mdb.models['Model-1'].parts['L1'].faces.getSequenceFromMask(('[#1 ]', ), ), 
        name='L1')
    mdb.models['Model-1'].parts['L1'].SectionAssignment(offset=0.0, offsetField='', 
        offsetType=MIDDLE_SURFACE, region=
        mdb.models['Model-1'].parts['L1'].sets['L1'], sectionName='memb_L1', 
        thicknessAssignment=FROM_SECTION)
    mdb.models['Model-1'].parts['L1_sh'].Set(faces=
        mdb.models['Model-1'].parts['L1_sh'].faces.getSequenceFromMask(('[#1 ]', ), 
        ), name='L1_sh')
    mdb.models['Model-1'].parts['L1_sh'].SectionAssignment(offset=0.0, offsetField=
        '', offsetType=MIDDLE_SURFACE, region=
        mdb.models['Model-1'].parts['L1_sh'].sets['L1_sh'], sectionName='shell_L1', 
        thicknessAssignment=FROM_SECTION)
    mdb.models['Model-1'].parts['L2'].Set(faces=
        mdb.models['Model-1'].parts['L2'].faces.getSequenceFromMask(('[#1 ]', ), ), 
        name='L2')
    mdb.models['Model-1'].parts['L2'].SectionAssignment(offset=0.0, offsetField='', 
        offsetType=MIDDLE_SURFACE, region=
        mdb.models['Model-1'].parts['L2'].sets['L2'], sectionName='memb_L2', 
        thicknessAssignment=FROM_SECTION)
    mdb.models['Model-1'].parts['L2_sh'].Set(faces=
        mdb.models['Model-1'].parts['L2_sh'].faces.getSequenceFromMask(('[#1 ]', ), 
        ), name='L2_sh')
    mdb.models['Model-1'].parts['L2_sh'].SectionAssignment(offset=0.0, offsetField=
        '', offsetType=MIDDLE_SURFACE, region=
        mdb.models['Model-1'].parts['L2_sh'].sets['L2_sh'], sectionName='shell_L2', 
        thicknessAssignment=FROM_SECTION)

    # Moulds
    mdb.models['Model-1'].parts['bot_rigid'].Set(faces=
        mdb.models['Model-1'].parts['bot_rigid'].faces.getByBoundingSphere((0.0,0.0,0.0),1000), name='bot')
    mdb.models['Model-1'].parts['bot_rigid'].SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=
        mdb.models['Model-1'].parts['bot_rigid'].sets['bot'], sectionName='rigid', 
        thicknessAssignment=FROM_SECTION)
    mdb.models['Model-1'].parts['top_rigid'].Set(faces=
        mdb.models['Model-1'].parts['top_rigid'].faces.getByBoundingSphere((0.0,0.0,0.0),1000), name='top')
    mdb.models['Model-1'].parts['top_rigid'].SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=
        mdb.models['Model-1'].parts['top_rigid'].sets['top'], sectionName='rigid', 
        thicknessAssignment=FROM_SECTION)




    ############# CREATE MESH #############

    # Prepreg
    size_mesh_prepreg = 3.0 #1.5
    mdb.models['Model-1'].parts['L1'].seedPart(deviationFactor=0.1, minSizeFactor=
        0.1, size=size_mesh_prepreg)
    
    mdb.models['Model-1'].parts['L1'].setElementType(elemTypes=(ElemType(
        elemCode=M3D4R, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF), ElemType(
        elemCode=M3D3, elemLibrary=EXPLICIT)), regions=(
        mdb.models['Model-1'].parts['L1'].faces.getSequenceFromMask(('[#1 ]', ), ), 
        ))
    mdb.models['Model-1'].parts['L1'].generateMesh()
    mdb.models['Model-1'].parts['L1_sh'].setElementType(elemTypes=(ElemType(
        elemCode=S4R, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, 
        hourglassControl=DEFAULT), ElemType(elemCode=S3R, elemLibrary=EXPLICIT)), 
        regions=(mdb.models['Model-1'].parts['L1_sh'].faces.getSequenceFromMask((
        '[#1 ]', ), ), ))

    mdb.models['Model-1'].parts['L1_sh'].seedPart(deviationFactor=0.1, 
        minSizeFactor=0.1, size=size_mesh_prepreg)
    mdb.models['Model-1'].parts['L1_sh'].generateMesh()
    mdb.models['Model-1'].parts['L2'].setElementType(elemTypes=(ElemType(
        elemCode=M3D4R, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, 
        hourglassControl=DEFAULT), ElemType(elemCode=M3D3, elemLibrary=EXPLICIT)), 
        regions=(mdb.models['Model-1'].parts['L2'].faces.getSequenceFromMask((
        '[#1 ]', ), ), ))

    mdb.models['Model-1'].parts['L2'].seedPart(deviationFactor=0.1, minSizeFactor=
        0.1, size=size_mesh_prepreg)
    mdb.models['Model-1'].parts['L2'].generateMesh()
    mdb.models['Model-1'].parts['L2_sh'].setElementType(elemTypes=(ElemType(
        elemCode=S4R, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, 
        hourglassControl=DEFAULT), ElemType(elemCode=S3R, elemLibrary=EXPLICIT)), 
        regions=(mdb.models['Model-1'].parts['L2_sh'].faces.getSequenceFromMask((
        '[#1 ]', ), ), ))

    mdb.models['Model-1'].parts['L2_sh'].seedPart(deviationFactor=0.1, 
        minSizeFactor=0.1, size=size_mesh_prepreg)
    mdb.models['Model-1'].parts['L2_sh'].generateMesh()

    # Moulds
    size_mesh_mould = 10.0 #5.0

    mdb.models['Model-1'].parts['top_rigid'].seedPart(deviationFactor=0.1, 
        minSizeFactor=0.1, size=size_mesh_mould)
    mdb.models['Model-1'].parts['top_rigid'].setElementType(elemTypes=(ElemType(
        elemCode=S4R, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, 
        hourglassControl=DEFAULT), ElemType(elemCode=S3R, elemLibrary=EXPLICIT)), 
        regions=(
        mdb.models['Model-1'].parts['top_rigid'].faces.getByBoundingSphere((0.0,0.0,0.0),1000), ))
    mdb.models['Model-1'].parts['top_rigid'].generateMesh()

    mdb.models['Model-1'].parts['bot_rigid'].seedPart(deviationFactor=0.1, 
        minSizeFactor=0.1, size=size_mesh_mould)
    mdb.models['Model-1'].parts['bot_rigid'].setElementType(elemTypes=(ElemType(
        elemCode=S4R, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, 
        hourglassControl=DEFAULT), ElemType(elemCode=S3R, elemLibrary=EXPLICIT)), 
        regions=(
        mdb.models['Model-1'].parts['bot_rigid'].faces.getByBoundingSphere((0.0,0.0,0.0),1000), ))
    mdb.models['Model-1'].parts['bot_rigid'].generateMesh()



    ############# CREATE ASSEMBLY #############

    # Call parts
    mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='L1-1', part=
        mdb.models['Model-1'].parts['L1'])
    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='L1_sh-1', part=
        mdb.models['Model-1'].parts['L1_sh'])
    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='L2-1', part=
        mdb.models['Model-1'].parts['L2'])
    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='L2_sh-1', part=
        mdb.models['Model-1'].parts['L2_sh'])
    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='bot_rigid-1', 
        part=mdb.models['Model-1'].parts['bot_rigid'])
    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='top_rigid-1', 
        part=mdb.models['Model-1'].parts['top_rigid'])


    # Place parts
    # mdb.models['Model-1'].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 
    #     0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('bot_rigid-1', 'top_rigid-1'))
    mdb.models['Model-1'].rootAssembly.translate(instanceList=('L1-1', 'L1_sh-1', 
        'L2-1', 'L2_sh-1'), vector=(-l/2, -l/2, 0.0))
    mdb.models['Model-1'].rootAssembly.translate(instanceList=('L2-1', 'L2_sh-1'), 
    vector=(0.0, 0.0, -thickness_prepreg))

    mdb.models['Model-1'].rootAssembly.translate(instanceList=('top_rigid-1', ), 
        vector=(0.0, 0.0, -thickness_prepreg - (thickness_prepreg+thickness_rigid)/2)) #-1
    mdb.models['Model-1'].rootAssembly.translate(instanceList=('bot_rigid-1', ), 
        vector=(0.0, 0.0, h+(thickness_rigid+thickness_prepreg)/2))
    

    # Merge composite plies (superimposition membrane + shell)
    mdb.models['Model-1'].rootAssembly._previewMergeMeshes(instances=(
        mdb.models['Model-1'].rootAssembly.instances['L1-1'], 
        mdb.models['Model-1'].rootAssembly.instances['L1_sh-1']), 
        mergeBoundaryOnly=False, nodeMergingTolerance=1e-06, 
        removeDuplicateElements=False)
    mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=MESH, 
        instances=(mdb.models['Model-1'].rootAssembly.instances['L1-1'], 
        mdb.models['Model-1'].rootAssembly.instances['L1_sh-1']), mergeNodes=ALL, 
        name='sup_L1', nodeMergingTolerance=1e-06, originalInstances=SUPPRESS, 
        removeDuplicateElements=False)
    mdb.models['Model-1'].rootAssembly._previewMergeMeshes(instances=(
        mdb.models['Model-1'].rootAssembly.instances['L2-1'], 
        mdb.models['Model-1'].rootAssembly.instances['L2_sh-1']), 
        mergeBoundaryOnly=False, nodeMergingTolerance=1e-06, 
        removeDuplicateElements=False)
    mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=MESH, 
        instances=(mdb.models['Model-1'].rootAssembly.instances['L2-1'], 
        mdb.models['Model-1'].rootAssembly.instances['L2_sh-1']), mergeNodes=ALL, 
        name='sup_L2', nodeMergingTolerance=1e-06, originalInstances=SUPPRESS, 
        removeDuplicateElements=False)
    mdb.models['Model-1'].ExplicitDynamicsStep(improvedDtMethod=ON, name='Step-1', 
        previous='Initial', timePeriod=8.0)

    # Create contact surfaces 
    mdb.models['Model-1'].rootAssembly.Surface(name='l1u', side2Elements=
        mdb.models['Model-1'].rootAssembly.instances['sup_L1-1'].elements[0:7938]) #32258
    mdb.models['Model-1'].rootAssembly.Surface(name='l1b', side1Elements=
        mdb.models['Model-1'].rootAssembly.instances['sup_L1-1'].elements[0:7938])
    mdb.models['Model-1'].rootAssembly.Surface(name='l2u', side2Elements=
        mdb.models['Model-1'].rootAssembly.instances['sup_L2-1'].elements[0:7938])
    mdb.models['Model-1'].rootAssembly.Surface(name='l2b', side1Elements=
        mdb.models['Model-1'].rootAssembly.instances['sup_L2-1'].elements[0:7938])

    mdb.models['Model-1'].rootAssembly.Surface(name='toprigid', side1Faces=
        mdb.models['Model-1'].rootAssembly.instances['top_rigid-1'].faces.getByBoundingSphere((0.0,0.0,0.0),1000))
    mdb.models['Model-1'].rootAssembly.Surface(name='botrigid', side2Faces=
        mdb.models['Model-1'].rootAssembly.instances['bot_rigid-1'].faces.getByBoundingSphere((0.0,0.0,0.0),1000))

    mdb.models['Model-1'].rootAssembly.regenerate()


    # Create contact 
    mdb.models['Model-1'].ContactProperty('IntProp-1')
    mdb.models['Model-1'].interactionProperties['IntProp-1'].TangentialBehavior(
        dependencies=0, directionality=ISOTROPIC, elasticSlipStiffness=None, 
        formulation=PENALTY, fraction=0.005, maximumElasticSlip=FRACTION, 
        pressureDependency=OFF, shearStressLimit=None, slipRateDependency=OFF, 
        table=((5.0, ), ), temperatureDependency=OFF)
    mdb.models['Model-1'].ContactExp(createStepName='Step-1', name='Int-1')
    mdb.models['Model-1'].interactions['Int-1'].includedPairs.setValuesInStep(
        addPairs=((
        mdb.models['Model-1'].rootAssembly.surfaces['botrigid'], 
        mdb.models['Model-1'].rootAssembly.surfaces['l1b']), (
        mdb.models['Model-1'].rootAssembly.surfaces['l1u'], 
        mdb.models['Model-1'].rootAssembly.surfaces['l2b']), (
        mdb.models['Model-1'].rootAssembly.surfaces['toprigid'], 
        mdb.models['Model-1'].rootAssembly.surfaces['l2u'])), stepName='Step-1', 
        useAllstar=OFF)
    mdb.models['Model-1'].interactions['Int-1'].contactPropertyAssignments.appendInStep(
        assignments=((GLOBAL, SELF, 'IntProp-1'), ), stepName='Step-1')
    mdb.models['Model-1'].interactions['Int-1'].move('Step-1', 'Initial')
    
    mdb.models['Model-1'].interactionProperties['IntProp-1'].tangentialBehavior.setValues(
        dependencies=0, directionality=ISOTROPIC, elasticSlipStiffness=None, 
        formulation=PENALTY, fraction=0.005, maximumElasticSlip=FRACTION, 
        pressureDependency=OFF, shearStressLimit=None, slipRateDependency=OFF, 
        table=((5.0, ), ), temperatureDependency=OFF)
    mdb.models['Model-1'].interactionProperties['IntProp-1'].NormalBehavior(
        allowSeparation=ON, constraintEnforcementMethod=DEFAULT, 
        pressureOverclosure=HARD)


    # Set creation; dependence of mould on 1 reference point
    mdb.models['Model-1'].rootAssembly.ReferencePoint(point=(0.0, 0.0, -0.57))
    top_reference = mdb.models['Model-1'].rootAssembly.referencePoints.values()[0]
    mdb.models['Model-1'].rootAssembly.ReferencePoint(point=(0.0, 0.0, 34.0))
    bottom_reference = mdb.models['Model-1'].rootAssembly.referencePoints.values()[0]

    mdb.models['Model-1'].rootAssembly.Set(name='m_Set-1', referencePoints=(
        top_reference, ))
    # mdb.models['Model-1'].rootAssembly.Set(faces=
    #     mdb.models['Model-1'].rootAssembly.instances['top_rigid-1'].faces.getByBoundingSphere((0.0,0.0,0.0),1000), name='s_Set-1')
    # mdb.models['Model-1'].Coupling(controlPoint=
    #     mdb.models['Model-1'].rootAssembly.sets['m_Set-1'], couplingType=KINEMATIC, 
    #     influenceRadius=WHOLE_SURFACE, localCsys=None, name='Constraint-1', 
    #     surface=mdb.models['Model-1'].rootAssembly.sets['s_Set-1'], u1=ON, u2=ON, 
    #     u3=ON, ur1=ON, ur2=ON, ur3=ON)

    mdb.models['Model-1'].rootAssembly.Set(name='m_Set-2', referencePoints=(
        bottom_reference, ))
    # mdb.models['Model-1'].rootAssembly.Set(faces=
    #     mdb.models['Model-1'].rootAssembly.instances['bot_rigid-1'].faces.getByBoundingSphere((0.0,0.0,0.0),1000), name='s_Set-2')
    # mdb.models['Model-1'].Coupling(controlPoint=
    #     mdb.models['Model-1'].rootAssembly.sets['m_Set-2'], couplingType=KINEMATIC, 
    #     influenceRadius=WHOLE_SURFACE, localCsys=None, name='Constraint-2', 
    #     surface=mdb.models['Model-1'].rootAssembly.sets['s_Set-2'], u1=ON, u2=ON, 
    #     u3=ON, ur1=ON, ur2=ON, ur3=ON)
    mdb.models['Model-1'].RigidBody(bodyRegion=
        mdb.models['Model-1'].rootAssembly.instances['top_rigid-1'].sets['top'], 
        name='Constraint-1', refPointRegion=
        mdb.models['Model-1'].rootAssembly.sets['m_Set-1'])
    
    mdb.models['Model-1'].RigidBody(bodyRegion=
        mdb.models['Model-1'].rootAssembly.instances['bot_rigid-1'].sets['bot'], 
        name='Constraint-2', refPointRegion=
        mdb.models['Model-1'].rootAssembly.sets['m_Set-2'])
    

    # Boundary conditions
    mdb.models['Model-1'].EncastreBC(createStepName='Initial', localCsys=None, 
        name='BC-1', region=mdb.models['Model-1'].rootAssembly.sets['m_Set-2'])

    mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
        distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-2', 
        region=mdb.models['Model-1'].rootAssembly.sets['m_Set-1'], u1=SET, u2=SET, 
        u3=UNSET, ur1=SET, ur2=SET, ur3=SET)

    mdb.models['Model-1'].TabularAmplitude(data=((0.0, 0.0), (8.0, 1.0)), name=
        'Amp-1', smooth=SOLVER_DEFAULT, timeSpan=STEP)

    mdb.models['Model-1'].DisplacementBC(amplitude='Amp-1', createStepName='Step-1'
        , distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
        'BC-3', region=mdb.models['Model-1'].rootAssembly.sets['m_Set-1'], u1=UNSET
        , u2=UNSET, u3=h-((thickness_prepreg + thickness_rigid)/2 + 0.07), ur1=UNSET, ur2=UNSET, ur3=UNSET)
    #mdb.models['Model-1'].boundaryConditions['BC-3'].setValues(u3=-7.0)
    
    
    
    ############# CREATE JOB #############
    mdb.Job(activateLoadBalancing=False, atTime=None, contactPrint=OFF, 
        description='', echoPrint=OFF, explicitPrecision=DOUBLE_PLUS_PACK, 
        historyPrint=OFF, memory=90, memoryUnits=PERCENTAGE, model='Model-1', 
        modelPrint=OFF, multiprocessingMode=THREADS, name=Job_name_corrected, 
        nodalOutputPrecision=SINGLE, numCpus=8, numDomains=8, 
        parallelizationMethodExplicit=DOMAIN, queue=None, resultsFormat=ODB, 
        scratch='', type=ANALYSIS, userSubroutine=
        '/home/elias/Abaqus_forming_test/my_subs.f', waitHours=0, waitMinutes=0)

    mdb.models['Model-1'].TimePoint(name='TimePoints-1', points=((6.8, ), (8.0, 
        )))
    mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(timeMarks=ON, 
        timePoint='TimePoints-1', variables=('CSTRESS', 'SDV'))#'S', 'E', 'LE', 'U', 'RF', 'SF', 'CSTRESS', 'SDV'))
    #mdb.models['Model-1'].historyOutputRequests['H-Output-1'].setValues(
     #   numIntervals=20, rebar=EXCLUDE, region=MODEL, sectionPoints=DEFAULT, 
      #  variables=('ALLIE', 'ALLKE'))

    Mass_scaling = 1e4
    mdb.models['Model-1'].steps['Step-1'].setValues(improvedDtMethod=ON, 
    massScaling=((SEMI_AUTOMATIC, MODEL, AT_BEGINNING, Mass_scaling, 0.0, None, 
    0, 0, 0.0, 0.0, 0, None), ))

    # Create .inp file
    mdb.jobs[Job_name_corrected].writeInput()
    
    mdb.close() 
    #del mdb.models['Model-1']#.rootAssembly
   




