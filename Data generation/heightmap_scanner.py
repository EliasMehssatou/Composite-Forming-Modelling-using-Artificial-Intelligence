'''
Heightmap extraction and preprocessing algorithm

@author: Elias Mehssatou; Vrije Universiteit Brussel & Universite Libre de Bruxelles, Belgium

Master thesis: Composite forming modelling using artificial intelligence

Prerequisites 
- Abaqus Input File (*.inp)
    - Mould must be Abaqus part labeled "top_rigid"
    - The part "top_rigid" must be located under the xy-plane
    - x and y dimensions must be smaller than 190 mm
- CNN with two-dimensional input shape (96,96)
'''
# Import libraries
import fileinput
from skimage.measure import block_reduce
from scipy.interpolate import griddata

# Provide file name for data extraction
filename = 'Job-43p0702636-17p68752126-30p208375-23p18715-28p87003-5p73031.inp' #'Job-double-dome.inp' 

# Extract nodal coordinates
part_flag = 0
co_flag = 0
counter = 0
with open(filename, 'r') as f:
    for line in f.readlines():
        if "*Element" in line:
            co_flag = 0
        if co_flag == 1:
            l = line.strip().split(',')
            l_float = [float(d) for d in l]
            if counter == 0:
                node_coordinates = np.array([l_float])
            if counter >= 1:
                a = np.array([l_float])
                node_coordinates = np.concatenate((node_coordinates, a), axis=0)
            counter += 1
        if "*Part, name=top_rigid" in line:
            part_flag = 1
        if part_flag == 1 and "*Node" in line:
            co_flag = 1
            part_flag = 0
      
print("Nodal coordinates extracted row-wise in the form [element number, x, y,z], shape of array: " + str(node_coordinates.shape)) # Nodal coordinates stored in node_coordinates with shape (amount of nodes, 4)

x = np.round(np.append(node_coordinates[:,1],[-95,95]) - min(node_coordinates[:,1]),2)
y = np.round(np.append(node_coordinates[:,2],[-95,95]) - min(node_coordinates[:,2]),2)
z = np.round(np.abs(node_coordinates[:,3]),2)
z = max(z) - z
z = np.append(z,[0,0])

print(x.shape)
print(y.shape)
print(z.shape)

# target grid to interpolate to
x_coords = np.arange(min(x),max(x))
y_coords = np.arange(min(y),max(y))
xi,yi = np.meshgrid(x_coords,y_coords)

# interpolate
zi = griddata((x,y),z,(xi,yi),method='cubic')
zi[np.isnan(zi)] = 0

# Make the grid square
print("zi has shape " + str(zi.shape) + " before making the grid square")
indice = int(''.join(map(str, np.where(zi.shape == np.amin(zi.shape))))[1])
delta = np.abs(zi.shape[0]-zi.shape[1])
side_flag = 0
while delta != 0:
    if indice == 0:
        if side_flag == 0:
            zi = np.row_stack((zi, np.zeros((1,zi.shape[1]))))
            side_flag = 1
        else:
            zi = np.row_stack((np.zeros((1,zi.shape[1])),zi))
            side_flag = 0
    elif indice == 1:
        if side_flag == 0:
            zi = np.column_stack((zi, np.zeros((zi.shape[0],1))))
            side_flag = 1
        else:
            zi = np.column_stack((np.zeros((zi.shape[0],1)),zi))
            side_flag = 0
    delta = np.abs(zi.shape[0]-zi.shape[1])
print("zi has shape " + str(zi.shape) + " after making the grid square")

# Preprocess the grid to match input shape of CNN (96,96)
input_shape = [96,96]
zi = np.pad(zi, (1,1), 'constant', constant_values=(0))
zi = block_reduce(zi, block_size=(2, 2), func=np.mean)
print("zi has shape " + str(zi.shape) + " after preprocessing")

# Plot coordinates and heightmap
fig = plt.figure(figsize=(12, 12))

ax1 = fig.add_subplot(1,2,1)
im = ax1.scatter(x,y,c=z,cmap=plt.get_cmap('gray'))
divider = make_axes_locatable(ax1)
cax = divider.append_axes('right', size='5%', pad=0.05)
cbar = fig.colorbar(im, cax=cax, orientation='vertical')
cbar.set_label(r"$\rm{height} \, h \, [\rm{mm}]$")
ax1.set_aspect('equal')
ax1.set_axis_off()
ax1.set_title(r"$\rm{Nodal\;\,coordinates}$")

ax2 = fig.add_subplot(1,2,2)
im = ax2.imshow(zi, cmap=plt.get_cmap('gray'), interpolation='bilinear')
divider = make_axes_locatable(ax2)
cax = divider.append_axes('right', size='5%', pad=0.05)
cbar = fig.colorbar(im, cax=cax, orientation='vertical')
cbar.set_label(r"$\rm{height} \, h \, [\rm{mm}]$")
ax2.set_aspect('equal')
ax2.set_axis_off()
ax2.set_title(r"$\rm{Preprocessed\;\,CNN\;\,input}$")

plt.show()