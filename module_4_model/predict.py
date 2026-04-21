import pickle
import numpy as np

# ================= LOAD MODEL =================
with open("module_4_model/crop_model.pkl", "rb") as f:
    model, FEATURES = pickle.load(f)


def predict_crops(soil_data, weather_data):
    try:
        # ================= VALIDATION =================
        if not soil_data or not weather_data:
            return []

        # ================= FEATURE VECTOR =================
        feature_map = {
            "N": soil_data["N"],
            "P": soil_data["P"],
            "K": soil_data["K"],
            "ph": soil_data["ph"],
            "temperature": weather_data["temperature"],
            "humidity": weather_data["humidity"],
            "rainfall": weather_data["rainfall"]
        }

        features = np.array([[feature_map[f] for f in FEATURES]])

        # ================= PREDICTION =================
        probs = model.predict_proba(features)[0]
        classes = model.classes_

        top_indices = np.argsort(probs)[::-1][:3]

        results = []
        for i in top_indices:
            results.append({
                "crop": classes[i],
                "confidence": round(probs[i] * 100, 2)
            })

        return results

    except Exception as e:
        print("Prediction error:", e)
        return []