import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
from keras import layers, models

class EvacuationCNN:
    def __init__(self, input_shape=(64, 64, 1)):
        self.model = self.build_model(input_shape)
    
    def build_model(self, input_shape):
        model = models.Sequential([
            # Convolutional layers
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            
            # Flatten and dense layers
            layers.Flatten(),
            layers.Dense(64, activation='relu'),
            layers.Dense(4, activation='softmax')  # 4 possible movement directions
        ])
        
        model.compile(optimizer='adam',
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])
        return model
    
    def predict_movement(self, state):
        # Preprocess state and predict best movement
        processed_state = self.preprocess_state(state)
        prediction = self.model.predict(processed_state)
        return self.decode_movement(prediction)
    
    def preprocess_state(self, state):
        # Convert state to CNN input format
        return state.reshape((-1, 64, 64, 1)) / 255.0
    
    def decode_movement(self, prediction):
        # Convert prediction to movement direction
        directions = ['up', 'down', 'left', 'right']
        return directions[prediction.argmax()]

    def train(self, training_data, labels):
        # Train the model
        self.model.fit(training_data, labels, epochs=10, validation_split=0.2)
        self.model.save('data/trained_models/evacuation_cnn.h5')