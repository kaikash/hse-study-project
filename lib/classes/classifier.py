import sys
sys.path.append('..')

import os
import tensorflow as tf
import keras_preprocessing
from keras_preprocessing import image
from keras_preprocessing.image import ImageDataGenerator
from PIL import Image, ImageOps
import numpy as np


class Classifier:
    model_path = 'data/model.h5'
    classes_amount = 3
    classes = ['circle', 'shake', 'square']

    def __init__(self):
        self.retraining = False
        if os.path.exists(Classifier.model_path):
            self.model = tf.keras.models.load_model(Classifier.model_path)
        else:
            self.model = None


    def retrain(self):
        if self.retraining:
            return

        self.retraining = True

        image_generator = ImageDataGenerator(rescale=1./255, validation_split=0.2)    
        train_dataset = image_generator.flow_from_directory(batch_size=16,
            directory='data/imgs',
            shuffle=True,
            target_size=(150, 150), 
            subset='training',
            class_mode='categorical')
        validation_dataset = image_generator.flow_from_directory(batch_size=16,
            directory='data/imgs',
            shuffle=True,
            target_size=(150, 150), 
            subset='validation',
            class_mode='categorical')
        model = tf.keras.models.Sequential([
            tf.keras.layers.Conv2D(32, 3, padding='same', activation='relu', input_shape=(150, 150, 3)),
            tf.keras.layers.MaxPooling2D(3, 3),
            tf.keras.layers.Conv2D(64, 3, padding='same', activation='relu'),
            tf.keras.layers.MaxPooling2D(3, 3),
            tf.keras.layers.Conv2D(128, 3, padding='same', activation='relu'),
            tf.keras.layers.MaxPooling2D(3, 3),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(516, activation='relu'),
            tf.keras.layers.Dense(Classifier.classes_amount, activation='softmax')
        ])

        model.summary()
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.fit(
            train_dataset,
            epochs=15,
            steps_per_epoch=20,
            validation_data=validation_dataset,
            verbose=1,
            validation_steps=3)
        model.save(Classifier.model_path)

        self.retraining = False
        self.model = model


    def predict(self, img_path):
        if self.model is None:
            raise 'Model does not exist'
        
        data = np.ndarray(shape=(1, 150, 150, 3), dtype=np.float32)
        image = Image.open(img_path)
        image = ImageOps.fit(image, (150, 150), Image.ANTIALIAS)
        image_array = np.asarray(image)
        data[0] = (image_array.astype(np.float32) / 127.0) - 1

        return self.model.predict(data)
