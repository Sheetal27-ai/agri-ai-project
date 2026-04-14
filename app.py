import streamlit as st
from module_1_image.predict import predict_soil
from module_2_soil.soil_map import get_soil_data
from module_3_weather.weather import get_weather
from module_4_model.predict import predict_crops
from module_5_profit.profit import calculate_profit

st.set_page_config(page_title="Smart Farming Advisor", page_icon="🌱")
st.title("🌱 Smart Farming Advisor")
st.caption("AI-based crop recommendation & profit optimization")

# ── INPUTS ──────────────────────────────────────────────────────────────────

uploaded_file = st.file_uploader("Upload land image", type=["jpg", "png"])
location      = st.text_input("Enter your city", "Ludhiana")

# ── MAIN FLOW ────────────────────────────────────────────────────────────────

if uploaded_file is not None:

    # Save image temporarily
    with open("temp.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image("temp.jpg", width=300)

    if st.button("🔍 Analyze Land"):

        with st.spinner("Analyzing..."):

            # ── Module 1: Soil image
            try:
                soil_type = predict_soil("temp.jpg")
            except Exception as e:
                st.error(f"Soil detection failed: {e}")
                st.stop()

            # ── Module 2: Soil data
            try:
                soil_data = get_soil_data(soil_type)
            except Exception as e:
                st.error(f"Soil data lookup failed: {e}")
                st.stop()

            # ── Module 3: Weather
            try:
                weather_data = get_weather(location)
            except Exception as e:
                st.error(f"Weather fetch failed: {e}")
                st.stop()

            # ── Module 4: Crop prediction
            try:
                top_crops = predict_crops(soil_data, weather_data)
            except Exception as e:
                st.error(f"Crop prediction failed: {e}")
                st.stop()

            # ── Module 5: Profit ranking
            try:
                final_crops = calculate_profit(top_crops)
            except Exception as e:
                st.error(f"Profit calculation failed: {e}")
                st.stop()

        # ── RESULTS ─────────────────────────────────────────────────────────

        st.subheader("📊 Results")

        # Weather summary
        col1, col2, col3 = st.columns(3)
        col1.metric("🌡️ Temperature", f"{weather_data['temperature']} °C")
        col2.metric("💧 Humidity",    f"{weather_data['humidity']} %")
        col3.metric("🌧️ Rainfall",    f"{weather_data['rainfall']} mm")

        st.write(f"**Soil Type:** {soil_type}")
        st.write(f"**Location:** {weather_data['city']} — {weather_data['description']}")

        st.divider()

        # Top 3 crops
        st.subheader("🌾 Top 3 Recommended Crops")

        medals = ["🥇", "🥈", "🥉"]

        for i, crop in enumerate(final_crops):
            profit_str = f"₹{crop['profit']:,}/hectare" if crop["profit"] else "Not available"
            st.write(
                f"{medals[i]} **{crop['crop'].capitalize()}** — "
                f"Confidence: `{crop['confidence']}%` | "
                f"Estimated Profit: `{profit_str}`"
            )