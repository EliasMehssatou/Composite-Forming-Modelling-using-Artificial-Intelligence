def find_correctness(actual,pred):
    correctness_function = 0
    delimiter = 0.05*np.amax(actual)
    print(delimiter)
    for i in range(64):
        for j in range(64):
            delta = np.abs(actual[i,j]-pred[i,j])
            
            if delta < delimiter: 
                correctness_function += 1
            else:
                print("[" + str(i) + ", " +str(j) + "]")

    return correctness_function/4096*100