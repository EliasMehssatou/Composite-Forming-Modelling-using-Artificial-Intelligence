best_nb_epoch = 10
best_batch_size = 5
best_learning_rate = 0.0005
best_filter_size = 8
best_nb_filter = 20

model = create_cnn(best_learning_rate, best_filter_size, best_nb_filter)
#model.summary()

history = model.fit(
   x_train, y_train, 
   batch_size = best_batch_size, 
   epochs = best_nb_epoch, 
   verbose = 1,
   validation_data = (x_val, y_val)
)

#model.save("CNN_fine-tuned") #"model_1"