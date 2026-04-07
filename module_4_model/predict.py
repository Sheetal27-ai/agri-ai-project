import pickle
import pandas as pd

# load trained model
with open("module_4_model/crop_model.pkl", "rb") as f:
    model = pickle.load(f)

def predict_crops(soil_data, weather_data):

    input_data = pd.DataFrame([{
        "N": soil_data["N"],
        "P": soil_data["P"],
        "K": soil_data["K"],
        "temperature": weather_data["temperature"],
        "humidity": weather_data["humidity"],
        "ph": soil_data["ph"],
        "rainfall": weather_data["rainfall"]
    }])

    # get probabilities
    probabilities = model.predict_proba(input_data)[0]

    # get crop names
    crops = model.classes_

    # combine crop + probability
    crop_probs = list(zip(crops, probabilities))

    # sort descending
    sorted_crops = sorted(crop_probs, key=lambda x: x[1], reverse=True)

    # top 3 crops
    top_3 = [crop[0] for crop in sorted_crops[:3]]

    return top_3