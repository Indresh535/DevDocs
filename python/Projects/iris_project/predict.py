import joblib
import pandas as pd

# Load model
model = joblib.load('model.pkl')

# Sample input (you can change this or get it from user input)
sample_data = pd.DataFrame({
    'sepal_length': [5.1],
    'sepal_width': [3.5],
    'petal_length': [1.4],
    'petal_width': [0.2]
})

# Predict
prediction = model.predict(sample_data)
print(f"Predicted Species: {prediction[0]}")
