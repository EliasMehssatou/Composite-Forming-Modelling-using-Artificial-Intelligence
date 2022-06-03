def txt_to_array(shearmap_name):
    counter = 0
    with open(shearmap_name, 'r') as f:
        for line in f.readlines():
            l = line.strip().replace('[','').replace(']','').replace(';','').split(',')
            l_float = np.abs([float(d) for d in l])
            if counter == 0:
                data = np.array([l_float])
            if counter >= 1:
                a = np.array([l_float])
                data = np.concatenate((data, a), axis=0)
            counter += 1
    return data


filename = 'LHS_data_1-5000.txt'

init = 0
with open(filename, 'r') as f:
    for sample in f.readlines():
        if init == 1:
            shearmap_title = "Job-" + sample.replace('[','').replace(']','').replace(';','').replace('.','p').replace(',','').replace(' ','-').replace('\n','')
            shearmap_title = shearmap_title + "-SHEARMAPL1.txt"
            shearmap_temp = txt_to_array(shearmap_title)
            init = 2
            shearmap_3d = np.concatenate((shearmap_3d[None], shearmap_temp[None]), axis=0)

        elif init == 0:
            shearmap_title = "Job-" + sample.replace('[','').replace(']','').replace(';','').replace('.','p').replace(',','').replace(' ','-').replace('\n','')
            shearmap_title = shearmap_title + "-SHEARMAPL1.txt"
            shearmap_3d = txt_to_array(shearmap_title)
            init = 1
            
        else: 
            shearmap_title = "Job-" + sample.replace('[','').replace(']','').replace(';','').replace('.','p').replace(',','').replace(' ','-').replace('\n','')
            shearmap_title = shearmap_title + "-SHEARMAPL1.txt"
            shearmap_temp = txt_to_array(shearmap_title)
            shearmap_3d = np.concatenate((shearmap_3d, shearmap_temp[None]), axis=0)
# print(shearmap_3d)
print('shearmap: ' + str(shearmap_3d.shape))
shearmap_3d_padded_temp = np.pad(shearmap_3d, (1,0), 'constant', constant_values=(0))
print(shearmap_3d_padded_temp.shape)
shearmap_3d_padded = np.delete(shearmap_3d_padded_temp,0,axis=0)
print(shearmap_3d_padded.shape)