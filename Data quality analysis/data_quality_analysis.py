doping_list = [0,100,200,300,400,500,611]#[0,50,70,100,200,300,400,500,611]
doping_list2 = [0,10,20,30,40,50,60]#[0,5,7,10,20,30,40,50,60]


x_amounts = []
y_avgs = []
y_flat = []
y_sphere = []
y_double_dome = []
y_errormin = []
y_errormin_label = []
y_errormax = []
y_errormax_label = []

for i in range (len(doping_list)):
    doping_amount = doping_list[i]
    
    if doping_amount == 0:
        CNN_model = keras.models.load_model("correct_model_tuned_1500")
    elif doping_amount == 50:
        CNN_model = keras.models.load_model("correct_doping_peak1000_50")
    elif doping_amount == 70:
        CNN_model = keras.models.load_model("correct_doping_peak1000_70")
    else:
        CNN_model = keras.models.load_model("correct_doping_replacing1000_" + str(doping_amount))

    x_amounts.append(doping_amount)

    pred_cnn_flat = CNN_model.predict(test_flat).reshape(64,64,1)*70
    correctness_flat = find_correctness(test_flat_result,pred_cnn_flat)

    pred_cnn_sphere = CNN_model.predict(test_sphere).reshape(64,64,1)*70
    correctness_sphere = find_correctness(test_sphere_result_e4,pred_cnn_sphere)
    
    pred_cnn_double_dome = CNN_model.predict(test_double_dome).reshape(64,64,1)*70
    correctness_double_dome = find_correctness(test_double_dome_result_e4,pred_cnn_double_dome)

    average = (correctness_flat+correctness_sphere + correctness_double_dome)/3
    y_flat.append(correctness_flat)
    y_sphere.append(correctness_sphere)
    y_double_dome.append(correctness_double_dome)
    y_avgs.append(average)

    if correctness_flat < correctness_sphere and correctness_flat < correctness_double_dome:
        y_errormin.append(np.abs(correctness_flat-average))
        y_errormin_label.append("flat")
    if correctness_flat > correctness_sphere and correctness_flat > correctness_double_dome:
        y_errormax.append(np.abs(correctness_flat-average))
        y_errormax_label.append("flat")

    if correctness_sphere < correctness_flat and correctness_sphere < correctness_double_dome:
        y_errormin.append(np.abs(correctness_sphere-average))
        y_errormin_label.append("sphere")
    if correctness_sphere > correctness_flat and correctness_sphere > correctness_double_dome:
        y_errormax.append(np.abs(correctness_sphere-average))
        y_errormax_label.append("sphere")

    if correctness_double_dome < correctness_flat and correctness_double_dome < correctness_sphere:
        y_errormin.append(np.abs(correctness_double_dome-average))
        y_errormin_label.append("double_dome")
    if correctness_double_dome > correctness_flat and correctness_double_dome > correctness_sphere:
        y_errormax.append(np.abs(correctness_double_dome-average))
        y_errormax_label.append("double_dome")

y_error =[y_errormin,y_errormax]
y_error2 =[[y_errormin[1],y_errormin[2]],[y_errormax[1],y_errormax[2]]]



plt.errorbar(doping_list2, y_avgs,
             yerr = y_error,
             fmt ='.', color='b',lw=0.5)
plt.plot(doping_list2, y_avgs,'--',lw=0.5,color='b')


plt.plot(doping_list2, y_flat,'--',lw=0.5,color='g')
plt.plot(doping_list2, y_sphere,'--',lw=0.5,color='r')
plt.plot(doping_list2, y_double_dome,'--',lw=0.5,color='c')
# plt.plot(x_amounts, y_avgs,'.',color='b')
#plt.title(r'batch size')
plt.ylabel(r'$\rm{Correctness\enspace [\%]}$')#,fontsize=20)
plt.xlabel(r'$\rm{Percentage\enspace of\enspace level\enspace 2\enspace data\enspace used\enspace for\enspace training\enspace [\%]}$')#,fontsize=20)
plt.grid(True)
plt.show()