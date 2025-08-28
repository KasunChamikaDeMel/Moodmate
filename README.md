# MoodMate: Your Empathetic Virtual Companion 🤖❤️

An empathetic virtual companion that provides real-time emotional support by analyzing facial expressions and voice tone.

## 🌟 Introduction

In an era dominated by screens, we often face increased stress, anger, and anxiety. While many mental health tools exist, they often lack real-time, personalized support that fits into our daily digital lives.

MoodMate is a final-year project designed to bridge this gap. It's a desktop application featuring an interactive 3D virtual pet that understands and responds to your emotional state in real-time. By leveraging machine learning models for facial and voice emotion recognition, MoodMate aims to provide immediate, empathetic feedback, whether it's a playful distraction or a motivational boost, making your digital experience healthier and more emotionally aware.

## ✨ Key Features

Real-Time Facial Emotion Recognition: Uses your webcam to detect emotions like stressness, sadness, anger and sleepiness.

Live Voice Emotion Analysis: Listens to your voice to identify emotional tones such as stress or sleepiness.

Interactive 3D Virtual Pet: A friendly companion that visually reacts to your detected emotions by changing its color and expression.

Personalized Interaction: Provides a unique and supportive experience tailored to your current mood.

## 🛠️ Technologies Used

This project is built with a combination of machine learning and graphical libraries in Python:

### Machine Learning:

TensorFlow / Keras: For building and training the emotion detection models.

OpenCV: For capturing and processing the live webcam feed for facial analysis.

Librosa & Sounddevice: For capturing and processing live audio for voice analysis.

Scikit-learn: For data preprocessing and model evaluation.

### Application & GUI:

Python: The core programming language.

Pyglet: For creating the 3D graphical user interface and rendering the virtual pet.

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

You need to have Python 3.8+ installed on your system.

### Installation
1. Clone the repository:
```
git clone https://github.com/your-username/MoodMate_Project.git
cd MoodMate_Project
```

2. Create a virtual environment (recommended):
```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the required dependencies:
```
pip install -r requirements.txt
```

### Usage
To launch the application, run the main script from the root directory:
```
python src/main.py
```

The application will start, open your webcam, and begin analyzing your facial expressions and voice. The 3D virtual pet will appear and react to your detected emotions.

## 📂 Project Structure
```
MoodMate_Project/
│
├── models/                # Trained model files (.h5, .pkl)
├── notebooks/             # Jupyter notebooks for model training
├── src/                   # Main source code
│   ├── gui.py             # Pyglet frontend code
│   ├── emotion_processor.py # Model loading and prediction logic
│   └── main.py            # Entry point to run the app
│
├── README.md              # This file
└── requirements.txt       # Python dependencies

```

## 🔮 Future Work

Enhance the virtual pet with more complex animations and interactions.

Expand the range of detectable emotions.

Implement a conversation module for the pet to provide verbal support.

Address computational costs and data privacy concerns for a more robust application.

## 👥 Contributors

Mr. Asitha Wijewardhana (Supervisor)

Ms. Shamila Serasinghe (Co-Supervisor)

| Index Number | Student Name |
|:--------------|:--------------|
| 22ug1-0281 | P.N.M.S.S. Wijesinghe |
| 22ug1-0323 |W.G.K.C. De Mel |
| 22ug1-0010 |T.H.R.C. Nirosha|


This project was developed as part of the final year curriculum at SLTC Research University.
