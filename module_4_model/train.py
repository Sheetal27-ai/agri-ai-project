import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
data = pd.read_csv("data/crop_data.csv")

# Features (input)
X = data.drop("label", axis=1)

# Target (output)
y = data["label"]

# Create model
model = RandomForestClassifier()

# Train model
model.fit(X, y)

# Save model
with open("module_4_model/crop_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved!")