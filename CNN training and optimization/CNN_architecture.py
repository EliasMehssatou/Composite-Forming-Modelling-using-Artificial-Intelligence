def create_cnn(learning_rate, filter_size, nb_filter):
    model = Sequential()
    model.add(Conv2D(nb_filter, (filter_size, filter_size), input_shape=input_shape_input, activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(3, 3)))
    model.add(Conv2D(nb_filter*4, (filter_size, filter_size), activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(nb_filter*8, (filter_size, filter_size), activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    # model.add(Dropout(0.5))
    model.add(UpSampling2D((2, 2)))
    model.add(Conv2D(nb_filter*8, (filter_size, filter_size), activation='relu', padding='same'))
    model.add(UpSampling2D((2, 2)))
    model.add(Conv2D(nb_filter*4, (filter_size, filter_size), activation='relu', padding='same'))
    model.add(UpSampling2D((2, 2)))
    model.add(Conv2D(1, (filter_size, filter_size), activation='relu', padding='same'))

    model.compile(loss = keras.losses.mean_squared_error, optimizer = keras.optimizers.Adam(learning_rate=learning_rate), metrics = ['accuracy'])
    # model.summary()
    return model 