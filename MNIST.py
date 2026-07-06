# imorting the dependencies
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import cv2 
from PIL import Image
import tensorflow as tf 
tf.random.set_seed(3)
from tensorflow import keras
from keras.datasets import mnist
from tensorflow.math import confusion_matrix
# loading the mnist data from keras.datasets
(X_train, Y_train), (X_test , Y_test) = mnist.load_data()
print(type(X_train))
print(X_train.shape , Y_train.shape , X_test.shape ,Y_test.shape)
# 60000 images are training data and 10000 images are testing data
#x_train: uint8 NumPy array of grayscale image data with shapes (60000, 28, 28), containing the training data. Pixel values range from 0 to 255.
#y_train: uint8 NumPy array of digit labels (integers in range 0-9) with shape (60000,) for the training data.
#x_test: uint8 NumPy array of grayscale image data with shapes (10000, 28, 28), containing the test data. Pixel values range from 0 to 255.
#y_test: uint8 NumPy array of digit labels (integers in range 0-9) with shape (10000,) for the test data.
#image dimension 28 * 28
# grayscale image = 1channel
print(X_train[10])
print(X_train[10].shape)
plt.imshow(X_train[25])
plt.show()
print(Y_train[25])
print(Y_train.shape, Y_test.shape)

# unique values in Y_train
print(np.unique(Y_train))
# unique values in Y_test
print(np.unique(Y_test))


# scaling the values
X_train = X_train/255
X_test = X_test/255

#printing the 10th image
print(X_train[10])

#building the neural network
# setting up the layers of the neural network

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28,28)),
    keras.layers.Dense(50 , activation='relu'),
    keras.layers.Dense(50 , activation='relu'),
    keras.layers.Dense(10 , activation='sigmoid')
])
# the above 10 shows the number of classes and it remains as it is but 50 is number of neurons in hidden layers and can be changed
# compiling the NN
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
# training the model
model.fit(X_train,Y_train , epochs=15)
# training data accuracy=98.9%
loss , accuracy = model.evaluate(X_test, Y_test)
print(accuracy)
# test data accuracy = 96.95%
print(X_test.shape)
# first data point in X_test
plt.imshow(X_test[0])
plt.show()
print(Y_test[0])

Y_pred = model.predict(X_test)
print(Y_pred.shape)
print(Y_pred[0])
# model.predict() gives the prediction probability of each class for that data point
# converting the prediction probability into class label, label means at which index the data is maximum in next line argmax show this
label_for_first_test_image = np.argmax(Y_pred[0])
print(label_for_first_test_image)
# converting the prediction probability into class label for all data points
Y_pred_labels = [np.argmax(i) for i in Y_pred]
print(Y_pred_labels)
# Y_test = true labels
# Y_pred_labels = predicted labels
# confusion matrix 
conf_matrix = confusion_matrix(Y_test,Y_pred_labels)
print(conf_matrix)
plt.figure(figsize=(15,7))
sns.heatmap(conf_matrix, annot=True, fmt='d' , cmap='Greens')
plt.ylabel('True labels')
plt.xlabel('Predicted labels')
plt.show()

# building a predictive system

input_image_path = r'C:\Users\Admin\Desktop\MNIST_Digit_Classification\flower.jpg'
input_image = cv2.imread(input_image_path)
print(type(input_image))
print(input_image)
cv2.namedWindow('Input Image', cv2.WINDOW_NORMAL)
cv2.imshow('Input Image', input_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(input_image.shape)
grayscale = cv2.cvtColor(input_image, cv2.COLOR_RGB2GRAY)
print(grayscale.shape)
input_image_resize = cv2.resize(grayscale, (28,28))
print(input_image_resize.shape)
cv2.namedWindow('Resized Image', cv2.WINDOW_NORMAL)
cv2.imshow('Resized Image', input_image_resize)
cv2.waitKey(0)
cv2.destroyAllWindows()
input_image_resize = input_image_resize/255
print(type(input_image_resize))
image_reshaped = np.reshape(input_image_resize, [1,28,28])
input_prediction = model.predict(image_reshaped)
print(input_prediction)
input_pred_label = np.argmax(input_prediction)  
print(input_pred_label)
#predictive system
input_image_path = input('Path of the image to be predicted:')
input_image = cv2.imread(input_image_path)
cv2.namedWindow('Input Image', cv2.WINDOW_NORMAL)
cv2.imshow('Input Image', input_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
grayscale = cv2.cvtColor(input_image, cv2.COLOR_RGB2GRAY)
input_image_resize = cv2.resize(grayscale, (28,28))
input_image_resize = input_image_resize/255
image_reshaped = np.reshape(input_image_resize, [1,28,28])
input_prediction = model.predict(image_reshaped)
input_pred_label = np.argmax(input_prediction)
print('The Handwritten Digit is recognized as ', input_pred_label)