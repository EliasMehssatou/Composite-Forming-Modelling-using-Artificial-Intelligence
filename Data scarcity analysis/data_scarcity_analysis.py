data_split = [100, 500, 1500, 2500, 3500, 4500]

x_amounts = []
y_avgs = []
y_avgs2 = []
y_flat = []
y_sphere = []
y_double_dome = []
y_errormin = []
y_errormin_label = []
y_errormax = []
y_errormax_label = []

y_errormin2 = []
y_errormin_label2 = []
y_errormax2 = []
y_errormax_label2 = []

for i in range (len(data_split)):
    train_amount = data_split[i]
    CNN_model = keras.models.load_model("correct_model_tuned_" + str(train_amount))

    x_amounts.append(train_amount)

    pred_cnn_flat = CNN_model.predict(test_flat).reshape(64,64,1)*y_max
    correctness_flat = find_correctness(test_flat_result,pred_cnn_flat)

    pred_cnn_sphere = CNN_model.predict(test_sphere).reshape(64,64,1)*y_max
    correctness_sphere = find_correctness(test_sphere_result,pred_cnn_sphere)
    
    pred_cnn_double_dome = CNN_model.predict(test_double_dome).reshape(64,64,1)*y_max
    correctness_double_dome = find_correctness(test_double_dome_result,pred_cnn_double_dome)

    average = (correctness_flat+correctness_sphere + correctness_double_dome)/3
    average2 = (correctness_sphere + correctness_double_dome)/2
    y_flat.append(correctness_flat)
    y_sphere.append(correctness_sphere)
    y_double_dome.append(correctness_double_dome)
    y_avgs.append(average)
    y_avgs2.append(average2)

    if correctness_flat < correctness_sphere and correctness_flat < correctness_double_dome:
        y_errormin.append(np.abs(correctness_flat-average))
        y_errormin_label.append("flat")
    if correctness_flat > correctness_sphere and correctness_flat > correctness_double_dome:
        y_errormax.append(np.abs(correctness_flat-average))
        y_errormax_label.append("flat")

    if correctness_sphere < correctness_flat and correctness_sphere < correctness_double_dome:
        y_errormin.append(np.abs(correctness_sphere-average))
        y_errormin_label.append("sphere")
        y_errormin2.append(np.abs(correctness_sphere-average))
        y_errormin_label2.append("sphere")
    if correctness_sphere > correctness_flat and correctness_sphere > correctness_double_dome:
        y_errormax.append(np.abs(correctness_sphere-average))
        y_errormax_label.append("sphere")
        y_errormin2.append(np.abs(correctness_sphere-average))
        y_errormin_label2.append("sphere")

    if correctness_double_dome < correctness_flat and correctness_double_dome < correctness_sphere:
        y_errormin.append(np.abs(correctness_double_dome-average))
        y_errormin_label.append("double_dome")
        y_errormin2.append(np.abs(correctness_double_dome-average))
        y_errormin_label2.append("double_dome")
    if correctness_double_dome > correctness_flat and correctness_double_dome > correctness_sphere:
        y_errormax.append(np.abs(correctness_double_dome-average))
        y_errormax_label.append("double_dome")
        y_errormax2.append(np.abs(correctness_double_dome-average))
        y_errormax_label2.append("double_dome")

y_error =[y_errormin,y_errormax]

print(y_errormin)
print(y_avgs)
plt.errorbar(x_amounts, y_avgs,
             yerr = y_error,
             fmt ='.', color='b',lw=0.5)
plt.plot(x_amounts, y_avgs,'--',lw=0.5,color='b')
plt.plot(x_amounts, y_flat,'--',lw=0.5,color='g')
plt.plot(x_amounts, y_sphere,'--',lw=0.5,color='r')
plt.plot(x_amounts, y_double_dome,'--',lw=0.5,color='c')
plt.ylabel(r'$\rm{Correctness\enspace [\%]}$')#,fontsize=20)
plt.xlabel(r'$\rm{Amount\enspace of\enspace training\enspace samples}$')#,fontsize=20)
plt.ylim(70,100)
plt.yticks([70,75,80,85,90,95,100])
plt.grid(True)
plt.show()