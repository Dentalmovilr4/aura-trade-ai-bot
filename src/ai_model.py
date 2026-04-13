import joblib
from sklearn.ensemble import RandomForestClassifier

class AIModel:
    def __init__(self):
        self.model = RandomForestClassifier()

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, features):
        return self.model.predict([features])[0]

    def save(self, path="models/model.pkl"):
        joblib.dump(self.model, path)

    def load(self, path="models/model.pkl"):
        self.model = joblib.load(path)