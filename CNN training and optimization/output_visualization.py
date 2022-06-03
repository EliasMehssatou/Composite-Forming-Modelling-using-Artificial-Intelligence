sample_to_predict = 1190

CNN_model_tuned = keras.models.load_model("CNN_fine-tuned")
CNN_model_baseline = keras.models.load_model("CNN_baseline")

CNN_model = CNN_model_tuned

pred_cnn = CNN_model.predict(x_train[sample_to_predict].reshape(1, img_rows_input, img_cols_input, 1)) 
pred_cnn = pred_cnn.reshape(64,64,1)*x_max



fig = plt.figure(figsize=(16, 12))
ax1 = fig.add_subplot(151)
#ax1.set_title(r'$\rm{input\,\,\,geometry}$')
im1 = ax1.imshow(x_train[sample_to_predict]*x_max, cmap=plt.get_cmap('gray'), interpolation='bilinear')
ax1.axis('off')
divider = make_axes_locatable(ax1)
cax = divider.append_axes('right', size='5%', pad=0.05)
cbar = fig.colorbar(im1, cax=cax, orientation='vertical')
cbar.set_label(r"$\rm{Tool\enspace elevation\enspace [mm]}$")

fig = plt.figure(figsize=(16, 12))
ax2 = fig.add_subplot(152)
#ax2.set_title(r'$\rm{simulation\,\,\,shearmap}$')
im2 = ax2.imshow(y_train[sample_to_predict]*70, cmap=plt.get_cmap('gray'), interpolation='bilinear', vmin = 0, vmax = np.amax(y_train[sample_to_predict]*y_max))
divider = make_axes_locatable(ax2)
cax = divider.append_axes('right', size='5%', pad=0.05)
cbar = fig.colorbar(im2, cax=cax, orientation='vertical')#,ticks=[0,0.5,1,1.5,2,2.5,3,3.5])
cbar.set_label(r"$\rm{Shear\enspace angle\enspace}[^\circ]$")
ax2.axis('off')

fig = plt.figure(figsize=(16, 12))
ax3 = fig.add_subplot(153)
#ax3.set_title(r'$\rm{reproduced\,\,\,shearmap}$')
im3 = ax3.imshow(pred_cnn, cmap=plt.get_cmap('gray'), interpolation='bilinear', vmin = 0, vmax = np.amax(y_train[sample_to_predict]*y_max))
divider = make_axes_locatable(ax3)
cax = divider.append_axes('right', size='5%', pad=0.05)
cbar = fig.colorbar(im2, cax=cax, orientation='vertical')
cbar.set_label(r"$\rm{Shear\enspace angle\enspace}[^\circ]$")
ax3.axis('off')
