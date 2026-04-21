import streamlit as st

# ================= BACKEND =================
from module_1_image.predict import predict_soil
from module_2_soil.soil_map import get_soil_data
from module_3_weather.weather import get_weather
from module_4_model.predict import predict_crops
from module_5_profit.profit import calculate_profit

from chatbot import chatbot_reply

# ================= CONFIG =================
st.set_page_config(page_title="AgriVision Pro", layout="wide")

# ================= LANGUAGE =================
LANGUAGES = {
    "English": {
        "dashboard": "Dashboard",
        "analysis": "Analysis",
        "results": "Results",
        "location": "Enter Location",
        "upload": "Upload Soil Image",
        "run": "Run AI Analysis",
        "insights": "AI Insights",
        "profit": "Profit Comparison",
        "warning": "Run Analysis first"
    },
    "Hindi": {
        "dashboard": "डैशबोर्ड",
        "analysis": "विश्लेषण",
        "results": "परिणाम",
        "location": "स्थान दर्ज करें",
        "upload": "मिट्टी की फोटो अपलोड करें",
        "run": "विश्लेषण शुरू करें",
        "insights": "एआई सुझाव",
        "profit": "लाभ तुलना",
        "warning": "पहले विश्लेषण करें"
    },
    "Punjabi": {
        "dashboard": "ਡੈਸ਼ਬੋਰਡ",
        "analysis": "ਵਿਸ਼ਲੇਸ਼ਣ",
        "results": "ਨਤੀਜੇ",
        "location": "ਥਾਂ ਦਰਜ ਕਰੋ",
        "upload": "ਮਿੱਟੀ ਦੀ ਤਸਵੀਰ ਅੱਪਲੋਡ ਕਰੋ",
        "run": "ਵਿਸ਼ਲੇਸ਼ਣ ਸ਼ੁਰੂ ਕਰੋ",
        "insights": "ਏਆਈ ਸੁਝਾਅ",
        "profit": "ਮੁਨਾਫਾ ਤੁਲਨਾ",
        "warning": "ਪਹਿਲਾਂ ਵਿਸ਼ਲੇਸ਼ਣ ਕਰੋ"
    }
}

if "lang" not in st.session_state:
    st.session_state.lang = "English"

lang = LANGUAGES[st.session_state.lang]

# ================= CSS =================
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg,#020403,#071a12); color:white;}
.card {
    background: rgba(255,255,255,0.05);
    border-radius:20px;
    padding:20px;
    box-shadow:0 10px 30px rgba(0,0,0,0.5);
    margin-bottom:15px;
}
.stButton>button {
    background: linear-gradient(135deg,#ffcc33,#d4a017);
    color:black;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ================= SESSION =================
if "chat_hist" not in st.session_state:
    st.session_state.chat_hist = []

# ================= NAVBAR =================
col1, col2, col3 = st.columns([2,6,2])

with col1:
    st.markdown("### 🌱 AgriVision Pro")

with col2:
    nav = st.radio(
        "",
        [lang["dashboard"], lang["analysis"], lang["results"]],
        horizontal=True
    )

with col3:
    st.selectbox("🌐", list(LANGUAGES.keys()), key="lang")

st.divider()

# ================= CHATBOT =================
with st.sidebar:
    st.title("🤖 AI Assistant")

    user_q = st.text_input("Ask anything...")

    if user_q:
        context = {}

        if "soil" in st.session_state:
            context["soil"] = st.session_state.soil
        if "weather" in st.session_state:
            context["weather"] = st.session_state.weather
        if "final" in st.session_state:
            context["crops"] = st.session_state.final

        res = chatbot_reply(user_q, context=context)
        st.session_state.chat_hist.append((user_q, res))

    for q, a in st.session_state.chat_hist[-5:]:
        st.write(f"🧑 {q}")
        st.write(f"🤖 {a}")

# ================= DASHBOARD =================
if nav == lang["dashboard"]:

    st.markdown("## 🚜 Farm Overview")

    soil = st.session_state.get("soil", "Not Analyzed")
    weather = st.session_state.get("weather", {})

    weather_text = weather.get("description", "--") if isinstance(weather, dict) else "--"

    col1, col2, col3 = st.columns(3)

    col1.markdown(f'<div class="card">🌱 Soil<br><b>{soil}</b></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="card">🌦 Weather<br><b>{weather_text}</b></div>', unsafe_allow_html=True)
    col3.markdown('<div class="card">💰 Profit<br><b>Check Results</b></div>', unsafe_allow_html=True)

# ================= ANALYSIS =================
elif nav == lang["analysis"]:

    st.markdown("## 🔬 Farm Analysis")

    # ================= LOCATION =================
    location = st.text_input(f"📍 {lang['location']}", "Ludhiana", key="location_input")

    # ================= WEATHER =================
    st.markdown("### 🌦 Weather")

    if st.button("Get Weather", key="weather_btn"):

        try:
            weather = get_weather(location)

            st.session_state["weather"] = weather
            

            st.success("✅ Weather fetched")

            st.write(f"📍 {weather['city']}")
            st.write(f"🌡 {weather['temperature']} °C")
            st.write(f"💧 {weather['humidity']} %")
            st.write(f"🌧 {weather['rainfall']} mm")

        except Exception as e:
            st.error(f"Weather Error: {e}")

    # ================= SOIL =================
    st.markdown("### 🌱 Soil")

    uploaded = st.file_uploader(lang["upload"], type=["jpg","png"], key="soil_upload")

    if uploaded:
        with open("temp.jpg","wb") as f:
            f.write(uploaded.getbuffer())

        st.image("temp.jpg", width=300)

        if st.button("Analyze Soil", key="soil_btn"):

            try:
                soil_result = predict_soil("temp.jpg")

                soil = soil_result["soil_type"]   # ✅ FIX
                soil = soil_result["soil_type"].lower()
                soil_data = get_soil_data(soil)

                if soil_data is None:
                    st.error("Soil data not found. Try another image.")
                    st.stop()


                st.session_state["soil"] = soil
                st.session_state["soil_data"] = soil_data
                st.session_state["soil_full"] = soil_result   # 🔥 extra info

                st.success(f"✅ Soil detected: {soil}")

                # 🔥 UI Upgrade
                st.markdown("### 🧪 Soil Insights")
                col1, col2, col3 = st.columns(3)

                col1.metric("💧 Moisture", soil_result["moisture"])
                col2.metric("🧱 Texture", soil_result["texture"])
                col3.metric("🌿 Organic", soil_result["organic_content"])
                st.markdown("### 🌾 Soil Nutrients (From Dataset)")

                col4, col5, col6, col7 = st.columns(4)

                col4.metric("N", round(soil_data["N"], 2))
                col5.metric("P", round(soil_data["P"], 2))
                col6.metric("K", round(soil_data["K"], 2))
                col7.metric("pH", round(soil_data["ph"], 2))

            except Exception as e:
                st.error(f"Soil Error: {e}")
# ================= RESULTS =================
elif nav == lang["results"]:
    if "weather" not in st.session_state or "soil_data" not in st.session_state:
        st.warning("⚠️ Please run Analysis first")
        st.stop()

    st.markdown("## 🌾 Crop Intelligence")

    if "soil_data" not in st.session_state:
        st.warning(lang["warning"])

    else:
        with st.spinner("Generating crops..."):

            crops = predict_crops(
                st.session_state["soil_data"],
                st.session_state["weather"]
)

            final = calculate_profit(crops, st.session_state["weather"])
            st.session_state.final = final

        cols = st.columns(3)
        medals = ["🥇","🥈","🥉"]

        for i, crop in enumerate(final[:3]):
            cols[i].markdown(f"""
            <div class="card">
            <h2>{medals[i]}</h2>
            <h3>{crop['crop']}</h3>
            💰 ₹{crop['profit']}<br>
            📊 {crop['confidence']}%
            </div>
            """, unsafe_allow_html=True)

        st.subheader(lang["profit"])
        st.bar_chart({c['crop']: c['profit'] for c in final[:3]})

        # ================= AI INSIGHTS =================
        st.markdown(f"### 🧠 {lang['insights']}")

        best = final[0]

        st.info(f"""
        ✔ Best crop: {best['crop']}  
        ✔ High profitability  
        ✔ Confidence: {best['confidence']}%  
        ✔ Suitable for current conditions  
        """)