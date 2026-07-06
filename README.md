# MNIST Digit Classifier

A web app that recognizes handwritten digits (0-9) using a Convolutional Neural Network, built with TensorFlow/Keras and served through Flask.

## Overview
This project takes a hand-drawn digit as input and predicts which number (0–9) it represents. It was built to explore image classification fundamentals and deploying a trained deep learning model as an interactive web app.

## Tech Stack
- Python
- TensorFlow / Keras (CNN model)
- Flask (backend/web server)
- HTML, CSS, JavaScript (frontend)

## How It Works
The model is a Convolutional Neural Network trained on the MNIST dataset (70,000 images of handwritten digits). The Flask app loads the trained model (`mnist_model.h5`) and serves a simple web interface where a user can draw a digit, which is then preprocessed (resized, normalized) and passed to the model for prediction.

## Results
- Trainin accuracy: 98.9%
- Test accuracy: 96.95%
- Trained over 15 epochs

## How to Run Locally
```bash
git clone https://github.com/erij-1111-N/Mnist-digit-classifier.git
cd Mnist-digit-classifier
pip install -r requirements.txt
python app.py