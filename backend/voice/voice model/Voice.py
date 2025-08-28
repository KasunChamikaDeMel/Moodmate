import librosa
import numpy as np
import os
import tensorflow as tf
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.model_selection import train_test_split
from collections import Counter
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.models import load_model

# CONFIGURATION

emotions = {
    "01": "sleepy",
    "05": "angry",
    "06": "stress"      #Emotions that wants to predict
}
dataset_path = r"C:\Users\User\Desktop\Moodmate\voice dataset"

# FEATURE EXTRACTION

def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path, duration=3, offset=0.5)
        y, _ = librosa.effects.trim(y)  # Trim silence
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
        mfcc = np.mean(mfcc.T, axis=0)
        return mfcc
    except Exception as e:
        print(f"Error extracting from {file_path}: {e}")
        return None


# LOAD DATASET

data, labels = [], []
for folder in os.listdir(dataset_path):
    folder_path = os.path.join(dataset_path, folder)
    if os.path.isdir(folder_path):
        for file in os.listdir(folder_path):
            if file.endswith(".wav"):
                emotion_code = file.split("-")[2]
                if emotion_code in emotions:
                    emotion_label = emotions[emotion_code]
                    feature = extract_features(os.path.join(folder_path, file))
                    if feature is not None:
                        data.append(feature)
                        labels.append(emotion_label)

# Check data distribution
print("Class Distribution:", Counter(labels))


# ENCODING

data = np.array(data)
labels = np.array(labels)

# Encode string labels to integers, then to one-hot
label_encoder = LabelEncoder()
labels_encoded = label_encoder.fit_transform(labels)

onehot_encoder = OneHotEncoder(sparse_output=False)
labels_encoded = onehot_encoder.fit_transform(labels_encoded.reshape(-1, 1))


# SPLIT AND RESHAPE

X_train, X_test, y_train, y_test = train_test_split(
    data, labels_encoded, test_size=0.2, random_state=42, stratify=labels_encoded
)

X_train = X_train.reshape(X_train.shape[0], 1, X_train.shape[1])
X_test = X_test.reshape(X_test.shape[0], 1, X_test.shape[1])


# BUILD & TRAIN MODEL

model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(1, 40)),
    Dropout(0.3),
    LSTM(64),
    Dropout(0.3),
    Dense(32, activation='relu'),
    Dense(len(emotions), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

history = model.fit(X_train, y_train, epochs=50, batch_size=16, validation_data=(X_test, y_test))


# EVALUATION

test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {test_acc * 100:.2f}%")


# PLOT

plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.title("LSTM Model Training Progress")
plt.grid(True)
plt.tight_layout()
plt.show()


# SAVE MODEL

model.save("voice_emotion_detector.h5")
print("Model saved successfully as 'voice_emotion_detector.h5'")


# LOAD AND VERIFY

model = load_model(r"C:\Users\User\Desktop\Moodmate\voice_emotion_detector.h5")
print("Model loaded successfully!")
