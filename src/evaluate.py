import numpy as np
import cv2
from ml_models.cnn_model import EvacuationCNN
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

def generate_test_data(num_samples=100):
    test_data = []
    true_labels = []

    for _ in range(num_samples):
        state = np.zeros((64, 64, 1), dtype=np.uint8)

        for _ in range(np.random.randint(1, 5)):
            x1, y1 = np.random.randint(0, 63), np.random.randint(0, 63)
            x2, y2 = np.random.randint(x1, 63), np.random.randint(y1, 63)
            cv2.rectangle(state, (x1, y1), (x2, y2), (255, 255, 255), -1)

        movement = np.random.choice(['up', 'down', 'left', 'right'])
        label = [0, 0, 0, 0]
        if movement == 'up':
            label[0] = 1
        elif movement == 'down':
            label[1] = 1
        elif movement == 'left':
            label[2] = 1
        elif movement == 'right':
            label[3] = 1

        test_data.append(state)
        true_labels.append(label)

    return np.array(test_data), np.array(true_labels)

def load_model():
    cnn_model = EvacuationCNN()
    cnn_model.model.load_weights('data/trained_models/evacuation_cnn.h5')
    return cnn_model

def get_predictions(cnn_model, test_data):
    predictions = cnn_model.model.predict(test_data)
    predicted_classes = np.argmax(predictions, axis=1)
    return predicted_classes

def get_confusion_matrix():
    test_data, true_labels = generate_test_data()
    cnn_model = load_model()
    predicted_classes = get_predictions(cnn_model, test_data)
    true_classes = np.argmax(true_labels, axis=1)
    cm = confusion_matrix(true_classes, predicted_classes)
    tpr, fpr, precision = compute_metrics(cm)

    print("Confusion Matrix:")
    print(cm)
    print("\nTrue Positive Rate (TPR) per class:", tpr)
    print("False Positive Rate (FPR) per class:", fpr)
    print("Precision per class:", precision)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap="Blues", xticklabels=['up', 'down', 'left', 'right'], yticklabels=['up', 'down', 'left', 'right'])
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.show()

    print("\nClassification Report:")
    print(classification_report(true_classes, predicted_classes, target_names=['up', 'down', 'left', 'right']))

def compute_metrics(conf_matrix):
    tpr = []
    fpr = []
    precision = []
    num_classes = conf_matrix.shape[0]
    
    for i in range(num_classes):
        tp = conf_matrix[i, i]
        fn = np.sum(conf_matrix[i, :]) - tp
        fp = np.sum(conf_matrix[:, i]) - tp
        tn = np.sum(conf_matrix) - (fp + fn + tp)
        
        tpr.append(tp / (tp + fn) if (tp + fn) > 0 else 0)
        fpr.append(fp / (fp + tn) if (fp + tn) > 0 else 0)
        precision.append(tp / (tp + fp) if (tp + fp) > 0 else 0)

    return tpr, fpr, precision

if __name__ == '__main__':
    get_confusion_matrix()