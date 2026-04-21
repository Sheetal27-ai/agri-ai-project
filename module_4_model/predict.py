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
            "temperature": weather_data.get("temperature", 25),
            "humidity": weather_data.get("humidity", 60),
            "rainfall": weather_data.get("rainfall", 100),
        }

        features = np.array([[feature_map.get(f, 0) for f in FEATURES]])

        # ================= PREDICTION =================
        probs = model.predict_proba(features)[0]
        classes = model.classes_

        top_indices = np.argsort(probs)[::-1][:3]

        results = []
        for i in top_indices:
            results.append({
                "crop": classes[i].lower(),
                "confidence": round(probs[i] * 100, 2)
            })

        return results

    except Exception as e:
        print("Prediction error:", e)
        return []