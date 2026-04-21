import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# ================= LOAD DATA =================
data = pd.read_csv("data/crop_data.csv")

# ================= FEATURE ORDER FIX =================
FEATURES = ["N", "P", "K", "ph", "temperature", "humidity", "rainfall"]

X = data[FEATURES]
y = data["label"]

# ================= MODEL =================
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# ================= SAVE =================
with open("module_4_model/crop_model.pkl", "wb") as f:
    pickle.dump((model, FEATURES), f)

print("✅ Model trained & saved with feature order!")