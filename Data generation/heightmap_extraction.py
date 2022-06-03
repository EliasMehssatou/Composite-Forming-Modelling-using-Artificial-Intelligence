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

        r = mth.hypot(ry, rx)
        q = mth.hypot(qy, qx)

        tx = min(1, max(0, (qx * r / q + ex) / a))
        ty = min(1, max(0, (qy * r / q + ey) / b))
        t = mth.hypot(ty, tx)
        tx /= t 
        ty /= t 

    return (mth.copysign(a * tx, p[0]), mth.copysign(b * ty, p[1]))

f = open("LHS_data_1-5000.txt", "r")
LHS_data = np.matrix(f.read())
init = 0 

for i in range (len(LHS_data)):
    ly = LHS_data[i,0]
    lx = LHS_data[i,1]
    alpha = LHS_data[i,2]
    alpha_rad = alpha*np.pi/180
    h = LHS_data[i,3]
    rtop = LHS_data[i,4]
    rbot = LHS_data[i,5]
    
    resolution = 48 # double for full resolution
    # Make 190x190 grid
    X = np.linspace(0,95,num = resolution)
    Y = np.linspace(0,95,num = resolution)
    
    heightmap = np.ones([len(X),len(Y)])
    
    for j in range (len(X)):
        for k in range(len(Y)):
            x = int(X[j])
            y = int(Y[k])
            if x**2/(lx/2)**2 + y**2/(ly/2)**2 <= 1:
                heightmap[len(X)-j-1,k] = h
            else:
                if alpha != 0:
                    closest_point = ellips_point_distance(lx/2, ly/2, [x,y])
                    d = np.sqrt((y-closest_point[1])**2+(x-closest_point[0])**2)
                    
                    if d <= rtop*np.cos(alpha_rad):
                        heightmap[len(X)-j-1,k] = h - (rtop - np.sqrt(rtop**2 - d**2))
                    elif d <= rtop/np.tan((alpha_rad + np.pi/2)/2) + h*np.tan(alpha_rad) + rbot/np.tan((alpha_rad + np.pi/2)/2) - rbot*np.cos(alpha_rad):
                        heightmap[len(X)-j-1,k] = (rtop/np.tan((alpha_rad + np.pi/2)/2) + h*np.tan(alpha_rad) - d)/np.tan(alpha_rad)
                    elif d <= rtop/np.tan((alpha_rad + np.pi/2)/2) + h*np.tan(alpha_rad) + rbot/np.tan((alpha_rad + np.pi/2)/2):
                        heightmap[len(X)-j-1,k] = rbot - np.sqrt(rbot**2 - (rtop/np.tan((alpha_rad + np.pi/2)/2) + h*np.tan(alpha_rad) + rbot/np.tan((alpha_rad + np.pi/2)/2)- d)**2)
                    elif d > rtop/np.tan((alpha_rad + np.pi/2)/2) + h*np.tan(alpha_rad) + rbot/np.tan((alpha_rad + np.pi/2)/2):
                        heightmap[len(X)-j-1,k] = 0
                else:
                    closest_point = ellips_point_distance(lx/2, ly/2, [x,y])
                    d = mth.dist(closest_point,[x,y])
                    if d <= rtop*np.cos(alpha_rad):
                        heightmap[len(X)-j-1,k] = h - (rtop - np.sqrt(rtop**2 - d**2))
                    elif d <= rtop+rbot:
                        heightmap[len(X)-j-1,k] = rbot - np.sqrt(rbot**2 - (rbot-d)**2)
                    elif d > rtop+rbot:
                        heightmap[len(X)-j-1,k] = 0
    
    
    Q1 = np.asanyarray(heightmap)
    Q2 = np.flipud(Q1)
    Q12 = np.concatenate((Q1, Q2), axis=0)
    Q12copy = Q12[:,:]
    Q34 = np.fliplr(Q12)
    total_heightmap = np.concatenate((Q34, Q12), axis=1)

    # print(total_heightmap)
    # print('total_heightmap: ' + str(total_heightmap.shape))
    
    if init == 1:
        heightmap_3d = np.concatenate((heightmap_3d[None], total_heightmap[None]), axis=0)
        init = 2

    elif init == 0:
        heightmap_3d = total_heightmap
        init = 1
        
    else: 
        heightmap_3d = np.concatenate((heightmap_3d, total_heightmap[None]), axis=0)

print('heightmap: ' + str(heightmap_3d.shape))
        

