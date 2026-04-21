from module_1_image.predict import predict_soil
from module_2_soil.soil_map import get_soil_data
from module_3_weather.weather import get_weather
from module_4_model.predict import predict_crops
from module_5_profit.profit import calculate_profit
from database import init_db, save_prediction

def main():
    init_db()  # ✅ initialize database

    image_path = "test.jpg"
    location = "Punjab"

    # Step 1: Soil
    soil_type = predict_soil(image_path)
    print("Soil Type:", soil_type)

    # Step 2: Soil Data
    soil_data = get_soil_data(soil_type)
    print("Soil Data:", soil_data)

    # Step 3: Weather
    weather_data = get_weather(location)
    print("Weather Data:", weather_data)

    # Step 4: Crop Prediction
    crops = predict_crops(soil_data, weather_data)
    print("Predicted Crops:", crops)

    # Step 5: Profit Calculation
    profits = calculate_profit(crops)
    print("Profits:", profits)

    # Step 6: Get Top 3 Crops
    best_crops = [item["crop"] for item in profits[:3]]
    print("Top 3 Crops:", best_crops)

    # ✅ Step 7: Save to database
    if best_crops:
        save_prediction(soil_data, weather_data, {
            "best_crop": best_crops[0],
            "top_crops": best_crops
    })

if __name__ == "__main__":
    main()