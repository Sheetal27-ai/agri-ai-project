import pickle
import pandas as pd
import os

# Always find crop_model.pkl regardless of where script is called from
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "module_4_model", "crop_model.pkl")

# Load trained model
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


def predict_crops(soil_data: dict, weather_data: dict) -> list:
    """
    Predict top 3 recommended crops.

    Args:
        soil_data:    dict with keys → N, P, K, ph
        weather_data: dict with keys → temperature, humidity, rainfall

    Returns:
        List of top 3 crop names ranked by probability
        e.g. ['rice', 'maize', 'cotton']
    """
    input_data = pd.DataFrame([{
        "N":           soil_data["N"],
        "P":           soil_data["P"],
        "K":           soil_data["K"],
        "temperature": weather_data["temperature"],
        "humidity":    weather_data["humidity"],
        "ph":          soil_data["ph"],
        "rainfall":    weather_data["rainfall"]
    }])

    # Get probabilities for all crops
    probabilities = model.predict_proba(input_data)[0]

    # Get crop names
    crops = model.classes_

    # Combine crop + probability and sort descending
    crop_probs  = list(zip(crops, probabilities))
    sorted_crops = sorted(crop_probs, key=lambda x: x[1], reverse=True)

    # Return top 3 crop names with their confidence scores
    top_3 = [
        {"crop": crop, "confidence": round(prob * 100, 2)}
        for crop, prob in sorted_crops[:3]
    ]

    return top_3


# Test
if __name__ == "__main__":
    soil    = {"N": 90, "P": 42, "K": 43, "ph": 6.5}
    weather = {"temperature": 32.05, "humidity": 31, "rainfall": 15.0}

    results = predict_crops(soil, weather)

    print("Top 3 Recommended Crops:")
    for i, r in enumerate(results, 1):
        print(f"  {i}. {r['crop']}  ({r['confidence']}% confidence)")