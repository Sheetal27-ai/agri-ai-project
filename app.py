import streamlit as st
from module_1_image.predict import predict_soil
from module_2_soil.soil_map import get_soil_data
from module_3_weather.weather import get_weather
from module_4_model.predict import predict_crops
from module_5_profit.profit import calculate_profit

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="Smart Farming Advisor",
    page_icon="🌱",
    layout="wide"
)

# ----------------- SIMPLE MULTI-LANGUAGE SUPPORT -----------------
LANGUAGES = {
    "English": {
        "title": "🌱 Smart Farming Advisor",
        "caption": "AI-based crop recommendation & profit optimization",
        "upload": "Upload land image",
        "city": "Enter your city",
        "analyze": "🔍 Analyze Land",
        "results": "📊 Results",
        "top_crops": "🌾 Top 3 Recommended Crops",
        "soil": "Soil Type",
        "location": "Location",
        "login": "Login",
        "username": "Username",
        "password": "Password",
        "login_btn": "Login",
        "logout": "Logout"
    },
    "Hindi": {
        "title": "🌱 स्मार्ट खेती सलाहकार",
        "caption": "AI आधारित फसल सुझाव और लाभ विश्लेषण",
        "upload": "जमीन की फोटो अपलोड करें",
        "city": "अपना शहर दर्ज करें",
        "analyze": "🔍 विश्लेषण करें",
        "results": "📊 परिणाम",
        "top_crops": "🌾 शीर्ष 3 फसलें",
        "soil": "मिट्टी का प्रकार",
        "location": "स्थान",
        "login": "लॉगिन",
        "username": "यूज़रनेम",
        "password": "पासवर्ड",
        "login_btn": "लॉगिन करें",
        "logout": "लॉगआउट"
    }
}

# ----------------- SESSION STATE -----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "language" not in st.session_state:
    st.session_state.language = "English"

lang = LANGUAGES[st.session_state.language]

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.title("⚙️ Settings")

    st.session_state.language = st.selectbox(
        "Language / भाषा",
        list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index(st.session_state.language)
    )

    if st.session_state.logged_in:
        if st.button(lang["logout"]):
            st.session_state.logged_in = False
            st.rerun()

# ----------------- LOGIN PAGE -----------------
if not st.session_state.logged_in:
    st.title(lang["login"])

    username = st.text_input(lang["username"])
    password = st.text_input(lang["password"], type="password")

    # SIMPLE DEMO CREDENTIALS (replace with real auth later)
    if st.button(lang["login_btn"]):
        if username == "admin" and password == "admin":
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")

# ----------------- MAIN APP -----------------
else:
    st.title(lang["title"])
    st.caption(lang["caption"])

    uploaded_file = st.file_uploader(lang["upload"], type=["jpg", "png"])
    location = st.text_input(lang["city"], "Ludhiana")

    if uploaded_file is not None:

        with open("temp.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.image("temp.jpg", width=350)

        if st.button(lang["analyze"]):

            with st.spinner("Processing AI models..."):

                try:
                    soil_type = predict_soil("temp.jpg")
                    soil_data = get_soil_data(soil_type)
                    weather_data = get_weather(location)
                    top_crops = predict_crops(soil_data, weather_data)
                    final_crops = calculate_profit(top_crops)
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.stop()

            st.subheader(lang["results"])

            # Metrics UI
            col1, col2, col3 = st.columns(3)
            col1.metric("🌡️ Temperature", f"{weather_data['temperature']} °C")
            col2.metric("💧 Humidity", f"{weather_data['humidity']} %")
            col3.metric("🌧️ Rainfall", f"{weather_data['rainfall']} mm")

            st.write(f"**{lang['soil']}:** {soil_type}")
            st.write(f"**{lang['location']}:** {weather_data['city']} - {weather_data['description']}")

            st.divider()

            st.subheader(lang["top_crops"])

            medals = ["🥇", "🥈", "🥉"]

            for i, crop in enumerate(final_crops):
                profit_str = f"₹{crop['profit']:,}/hectare" if crop.get("profit") else "Not available"

                st.success(
                    f"{medals[i]} **{crop['crop'].capitalize()}** | "
                    f"Confidence: {crop['confidence']}% | "
                    f"Profit: {profit_str}"
                )
