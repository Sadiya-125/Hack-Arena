import numpy as np
import cv2, random
from ml_models.cnn_model import EvacuationCNN

def generate_training_data(num_samples=1000):
    training_data = []
    labels = []
    
    for _ in range(num_samples):
        # Generate a random state (64x64 image with obstacles)
        state = np.zeros((64, 64, 1), dtype=np.uint8)
        
        # Randomly place obstacles
        for _ in range(random.randint(1, 5)):
            x1, y1 = random.randint(0, 63), random.randint(0, 63)
            x2, y2 = random.randint(x1, 63), random.randint(y1, 63)
            cv2.rectangle(state, (x1, y1), (x2, y2), (255, 255, 255), -1)
        
        # Random movement direction
        movement = random.choice(['up', 'down', 'left', 'right'])
        label = [0, 0, 0, 0]  # One-hot encoding
        if movement == 'up':
            label[0] = 1
        elif movement == 'down':
            label[1] = 1
        elif movement == 'left':
            label[2] = 1
        elif movement == 'right':
            label[3] = 1
        
        training_data.append(state)
        labels.append(label)
    
    return np.array(training_data), np.array(labels)

def train_model():
    training_data, labels = generate_training_data()
    cnn_model = EvacuationCNN()
    history = cnn_model.train(training_data, labels)
    return history