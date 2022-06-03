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


design_parameters = [36.92, 0.576, 21.1166, 58.296, 7.02, 11.96]
design_parameters_temp = [36.92, 0.576, 21.1166, 58.296, 7.02, 11.96]

variations = [0.75,0.8,0.85,0.9,0.95,1.0,1.05,1.1,1.15,1.2,1.25]

LHS_data = np.zeros([len(design_parameters)*len(variations),len(design_parameters)])
# print(LHS_data.shape)
# print(LHS_data)
# LHS_data[0,:]= np.array([1000,1,2,50,3,4])
# print(LHS_data.shape)
# print(LHS_data)

counter = 0
for i in range(len(design_parameters)):
    for j in range(len(variations)):
        design_parameters_temp[i] *= variations[j]
        LHS_data[counter,:]= np.array(design_parameters_temp)
        design_parameters_temp[i] = design_parameters[i]
        counter += 1

print(LHS_data.shape)



init = 0
max_values = []

for i in range(len(LHS_data)):
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
    
    
    Q1 = np.asanyarray(heightmap)
    Q2 = np.flipud(Q1)
    Q12 = np.concatenate((Q1, Q2), axis=0)
    Q12copy = Q12[:,:]
    Q34 = np.fliplr(Q12)
    total_heightmap = np.concatenate((Q34, Q12), axis=1)

    

    total_heightmap /= x_max
    pred_cnn = CNN_model_tuned_5_0p0005_8_20.predict(total_heightmap.reshape(1, img_rows_input, img_cols_input, 1))
    pred_cnn = pred_cnn.reshape(64,64,1)*y_max
    max_values.append(np.amax(pred_cnn))




print(len(max_values))
# print(max_values)

length = len(variations)
#max_values /= actual_max
for i in range(len(max_values)):
    max_values[i] *= 57.160442 #actual_max

plt.plot(variations,max_values[0*length:1*length],lw=0.5,color='b',label = r'$l_{\rm{x}}$', alpha=0.7)
#plt.plot(nb_of_filters,params,'.',color='b')
plt.plot(variations,max_values[1*length:2*length],lw=0.5,color='g',label = r'$l_{\rm{y}}$', alpha=0.7)
plt.plot(variations,max_values[2*length:3*length],lw=0.5,color='r',label = r'$\alpha$', alpha=1.0)
plt.plot(variations,max_values[3*length:4*length],lw=0.5,color='c',label = r'$h$', alpha=1.0)
plt.plot(variations,max_values[4*length:5*length],lw=0.5,color='m',label = r'$r_{\rm{top}}$', alpha=0.7)
plt.plot(variations,max_values[5*length:6*length],lw=0.5,color='y',label = r'$r_{\rm{bot}}$', alpha=0.7)



plt.xlabel(r'$\frac{DV}{DV_{\rm{actual}}}$')
plt.ylabel(r'$\frac{\gamma_{\rm{max}}}{\gamma_{\rm{max,\,actual}}}$')
plt.xlim(0.75,1.25)
plt.grid(True)
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
#plt.legend(["1","2","3","4","5","6"], loc='upper right')
plt.savefig("sensitivity.pdf", format="pdf", bbox_inches="tight")
plt.show()
