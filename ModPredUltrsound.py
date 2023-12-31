# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mJsdeQ-lI8h1NGp0PED5Nfzt038m9mGP
"""
#S'intalen les llibreries a l'ambient de desenvolupament.
!pip install opendatasets
!pip install pandas

from google.colab import files
files.upload()

import opendatasets as od
import os
from pathlib import Path
import keras.utils as image
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.layers import BatchNormalization

od.download("https://www.kaggle.com/datasets/aryashah2k/breast-ultrasound-images-dataset")

p = Path("/content/breast-ultrasound-images-dataset/Dataset_BUSI_with_GT/")
dirs = p.glob("*")

imageData = []
labels = []
labelDict = {"normal":0, "benign":1, "malignant":2}

for folderDir in dirs:
  label = str(folderDir).split("/")[-1]
  print(label)
  for imgPath in folderDir.glob("*.png"):
    if "mask" not in str(imgPath):
      img = image.load_img(imgPath, target_size=(300,300))
      imgArray = image.img_to_array(img)
      imageData.append(imgArray)
      labels.append(labelDict[label])

def drawImg(img,label):
  plt.title(label)
  plt.imshow(img)
  plt.show

X = np.array(imageData)
y = np.array(labels)
print(X.shape)
drawImg(X[0]/255.0, y[0])
#Stay here bitch
X = X/255.0
x_train, x_test, y_train, y_test = train_test_split(X,y,test_size=0.25, random_state=42)

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(300, 300, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(BatchNormalization())
model.add(layers.Flatten())
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dense(3))

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

history = model.fit(x_train, y_train, epochs=12,
                    validation_data=(x_test, y_test))

model.fit(x_test, y_test)
