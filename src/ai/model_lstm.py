import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import load_model

class LSTMModel:
    def __init__(self):
        self.model = None

    def build(self, input_shape):
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
        model.add(LSTM(50))
        model.add(Dense(1, activation='sigmoid'))

        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        self.model = model

    def train(self, X, y):
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))
        self.build((X.shape[1], 1))
        self.model.fit(X, y, epochs=5, batch_size=32)

    def predict(self, features):
        features = np.array(features)
        features = np.reshape(features, (1, features.shape[0], 1))
        pred = self.model.predict(features)
        return 1 if pred[0][0] > 0.5 else 0

    def save(self, path="models/lstm_model.h5"):
        self.model.save(path)

    def load(self, path="models/lstm_model.h5"):
        self.model = load_model(path)