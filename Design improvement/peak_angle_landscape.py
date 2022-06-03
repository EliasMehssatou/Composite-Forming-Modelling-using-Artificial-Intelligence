from numpy import ma
from matplotlib import ticker, cm



sensitivity_params = [2,3]


design_parameters = [36.92, 0.576, 21.1166, 58.296, 7.02, 11.96]
design_parameters_temp = [36.92, 0.576, 21.1166, 58.296, 7.02, 11.96]

variations = np.linspace(0.5,1.5,100) #[0.5,0.55,0.6,0.7,0.75,0.8,0.85,0.9,0.95,1.05,1.1,1.15,1.2,1.25]

LHS_data = np.zeros([2*len(variations),len(design_parameters)])
# print(LHS_data.shape)
# print(LHS_data)
# LHS_data[0,:]= np.array([1000,1,2,50,3,4])
# print(LHS_data.shape)
# print(LHS_data)

counter = 0
for i in sensitivity_params:
    for j in range(len(variations)):
        design_parameters_temp[i] *= variations[j]
        LHS_data[counter,:]= np.array(design_parameters_temp)
        design_parameters_temp[i] = design_parameters[i]
        counter += 1

print(LHS_data.shape)


sensitivity_params = [2,3]

design_parameters = [36.92, 0.576, 21.1166, 58.296, 7.02, 11.96]
design_parameters_temp = [36.92, 0.576, 21.1166, 58.296, 7.02, 11.96]

N = 50
x = np.linspace(0.5*design_parameters[2], 1.5*design_parameters[2], N)
y = np.linspace(0.5*design_parameters[3], 1.5*design_parameters[3], N)


variations = np.linspace(0.5,1.5,100) 

LHS_data = np.zeros([N*N,len(design_parameters)])
# print(LHS_data.shape)
# print(LHS_data)
# LHS_data[0,:]= np.array([1000,1,2,50,3,4])
# print(LHS_data.shape)
# print(LHS_data)

counter = 0
for i in range(N):
    for j in range(N):
        design_parameters_temp[2] = x[j]
        design_parameters_temp[3] = y[i]
        LHS_data[counter,:]= np.array(design_parameters_temp)
        counter += 1



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


init = 0
max_values = []
CNN_model_tuned_5_0p0005_8_20 = keras.models.load_model("correct_model_tuned_5-0.0005-8-20")
img_rows_input, img_cols_input = resolution*2, resolution*2
img_rows_output, img_cols_output = 64, 64


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

length = len(variations)
actual_max = 50.6
# for i in range(len(max_values)):
#     max_values[i] *= actual_max

Z2 = np.array(max_values)
Z2 = Z2.reshape(50,50)

N = 50
x = np.linspace(0.5*design_parameters[2], 1.5*design_parameters[2], N)
y = np.linspace(0.5*design_parameters[3], 1.5*design_parameters[3], N)
X, Y = np.meshgrid(x, y)
Z = np.zeros([N,N])

# LHS_data[counter,:]= np.array(design_parameters_temp)

for i in range(N):
    for j in range(N-1):
        Z[i,:] = max_values[j*N:(j+1)*N]

print(X.shape)
print(Y.shape)
print(Z.shape)
print(Z2.shape)


design_parameters = [36.92, 0.576, 21.1166, 58.296, 7.02, 11.96]
# Define levels in z-axis where we want lines to appear
levels = np.array(["50"])#np.array(["$\rm{50}$"])

# Generate a color mapping of the levels we've specified
cpf = plt.contourf(X,Y,Z2, len(levels), cmap=cm.Reds)


# Set all level lines to black
line_colors = ['black' for l in cpf.levels]

# Make plot and customize axes
cp = plt.contour(X, Y, Z2, levels=levels, colors=line_colors)

fmt = {}
strs = ['50']
for l, s in zip(cp.levels, strs):
    fmt[l] = s


plt.clabel(cp, cp.levels[::2], inline=True, fmt=fmt, fontsize=10,colors=line_colors)


cs = plt.contourf(X, Y, Z2,cmap =cm.Reds)
#cbar = plt.colorbar(cs)

cbar = plt.colorbar(cs)
cbar.ax.set_ylabel(r'$\gamma_{\rm{max}}\enspace [^\circ]$')

plt.plot(21.1166, 58.296, marker = 'o', ms = 10, mec = 'black',mfc = 'r')

plt.plot(23.5, 48.1, marker = 'o', ms = 10, mec = 'black',mfc = 'g')
plt.xlabel(r'$\alpha\enspace [^\circ]$')
plt.ylabel(r'$h\enspace [\rm{mm}]$')
plt.show()