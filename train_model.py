import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

# Load your dataset
df = pd.read_csv("loan_data.csv")  # Make sure this file exists

# Select features and target
X = df[['income', 'credit_score']]
y = df['eligible']  # 1 = eligible, 0 = not eligible

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save model
os.makedirs("models", exist_ok=True)
with open("models/loan_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved to models/loan_model.pkl")