# Define training and validation sets 
train_amount = 2000
val_amount = 397
test_amount = 2500

x_train = load_original_heightmap_3d[0:train_amount,:,:]
y_train = load_original_shearmap_3d[0:train_amount,:,:]
x_val = load_original_heightmap_3d[train_amount+1:train_amount+1+val_amount,:,:]
y_val = load_original_shearmap_3d[train_amount+1:train_amount+1+val_amount,:,:]
x_test = load_original_heightmap_3d[train_amount+1+val_amount+1:train_amount+1+val_amount+1+test_amount,:,:]
y_test = load_original_shearmap_3d[train_amount+1+val_amount+1:train_amount+1+val_amount+1+test_amount,:,:]
print('x_train: ' + str(x_train.shape))
print('y_train: ' + str(y_train.shape))
print('x_val:  '  + str(x_val.shape))
print('y_val:  '  + str(y_val.shape))



# Process and reshape data 
img_rows_input, img_cols_input = resolution*2, resolution*2
img_rows_output, img_cols_output = 64, 64
from sklearn import preprocessing

# x_train = preprocessing.normalize(x_train)
# x_val = preprocessing.normalize(x_val)
# x_test = preprocessing.normalize(x_test)

if K.image_data_format() == 'channels_first': 
   x_train = x_train.reshape(x_train.shape[0], 1, img_rows_input, img_cols_input) 
   x_val = x_val.reshape(x_val.shape[0], 1, img_rows_input, img_cols_input) 
   x_test = x_test.reshape(x_test.shape[0], 1, img_rows_input, img_cols_input) 
   input_shape_input = (1, img_rows_input, img_cols_input) 

   y_train = y_train.reshape(y_train.shape[0], 1, img_rows_output, img_cols_output) 
   y_val = y_val.reshape(y_val.shape[0], 1, img_rows_output, img_cols_output) 
   y_test = y_test.reshape(y_test.shape[0], 1, img_rows_output, img_cols_output) 
   input_shape_output = (1, img_rows_output, img_cols_output)
else: 
   x_train = x_train.reshape(x_train.shape[0], img_rows_input, img_cols_input, 1) 
   x_val = x_val.reshape(x_val.shape[0], img_rows_input, img_cols_input, 1) 
   x_test = x_test.reshape(x_test.shape[0], img_rows_input, img_cols_input, 1) 
   input_shape_input = (img_rows_input, img_cols_input, 1) 

   y_train = y_train.reshape(y_train.shape[0], img_rows_output, img_cols_output, 1) 
   y_val = y_val.reshape(y_val.shape[0], img_rows_output, img_cols_output, 1) 
   y_test = y_test.reshape(y_test.shape[0], img_rows_output, img_cols_output, 1) 
   input_shape_output = (img_rows_output, img_cols_output, 1) 
   
x_train = x_train.astype('float32') 
x_val = x_val.astype('float32') 
x_test = x_test.astype('float32') 
x_max = max([np.amax(x_train),np.amax(x_val),np.amax(x_test)])
x_train /= x_max
x_val /= x_max
x_test /= x_max 

y_max = max([np.amax(y_train),np.amax(y_val),np.amax(y_test)])
y_train = y_train.astype('float32') 
y_val = y_val.astype('float32') 
y_test = y_test.astype('float32') 
y_train /= y_max
y_val /= y_max
y_test /= y_max


