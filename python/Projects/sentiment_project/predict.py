import joblib

# Load model and vectorizer
model = joblib.load('model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Input
text = ["I love this product!"]  # Example input
X_input = vectorizer.transform(text)

# Predict
prediction = model.predict(X_input)
print(f"Sentiment: {prediction[0]}")
