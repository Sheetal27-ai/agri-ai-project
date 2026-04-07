import streamlit as st
from module_1_image.predict import predict_soil
from module_2_soil.soil_map import get_soil_data
from module_3_weather.weather import get_weather
from module_4_model.predict import predict_crops
from module_5_profit.profit import calculate_profit, rank_crops

st.title("🌱 Smart Farming Advisor")

# Upload image
uploaded_file = st.file_uploader("Upload land image", type=["jpg", "png"])

# Location input
location = st.text_input("Enter location", "Punjab")

if uploaded_file is not None:

    # Save image temporarily
    with open("temp.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image("temp.jpg", width=300)

    if st.button("Analyze Land"):

        # Module 1
        soil_type = predict_soil("temp.jpg")

        # Module 2
        soil_data = get_soil_data(soil_type)

        # Module 3
        weather_data = get_weather(location)

        # Module 4
        crops = predict_crops(soil_data, weather_data)
        

        # Module 5
        profits = calculate_profit(crops)
        best_crops = rank_crops(profits)

        # Display results
        st.subheader("🌾 Results")

        st.write("Soil Type:", soil_type)
        st.write("Weather:", weather_data)

        st.write("### 🌱 Recommended Crops:")
        for crop in best_crops:
            st.write(f"- {crop} (Profit: ₹{profits[crop]})")