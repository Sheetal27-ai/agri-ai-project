# import streamlit as st

# # ================= BACKEND =================
# from module_1_image.predict import predict_soil
# from module_2_soil.soil_data import get_soil_data
# from module_3_weather.weather import get_weather
# from module_4_model.predict import predict_crops
# from module_5_profit.profit import calculate_profit

# from chatbot import chatbot_reply

# # ================= CONFIG =================
# st.set_page_config(page_title="AgriVision Pro", layout="wide")

# # ================= LANGUAGE =================
# LANGUAGES = {
#     "English": {
#         "dashboard": "Dashboard",
#         "analysis": "Analysis",
#         "results": "Results",
#         "location": "Enter Location",
#         "upload": "Upload Soil Image",
#         "run": "Run AI Analysis",
#         "insights": "AI Insights",
#         "profit": "Profit Comparison",
#         "warning": "Run Analysis first"
#     },
#     "Hindi": {
#         "dashboard": "डैशबोर्ड",
#         "analysis": "विश्लेषण",
#         "results": "परिणाम",
#         "location": "स्थान दर्ज करें",
#         "upload": "मिट्टी की फोटो अपलोड करें",
#         "run": "विश्लेषण शुरू करें",
#         "insights": "एआई सुझाव",
#         "profit": "लाभ तुलना",
#         "warning": "पहले विश्लेषण करें"
#     },
#     "Punjabi": {
#         "dashboard": "ਡੈਸ਼ਬੋਰਡ",
#         "analysis": "ਵਿਸ਼ਲੇਸ਼ਣ",
#         "results": "ਨਤੀਜੇ",
#         "location": "ਥਾਂ ਦਰਜ ਕਰੋ",
#         "upload": "ਮਿੱਟੀ ਦੀ ਤਸਵੀਰ ਅੱਪਲੋਡ ਕਰੋ",
#         "run": "ਵਿਸ਼ਲੇਸ਼ਣ ਸ਼ੁਰੂ ਕਰੋ",
#         "insights": "ਏਆਈ ਸੁਝਾਅ",
#         "profit": "ਮੁਨਾਫਾ ਤੁਲਨਾ",
#         "warning": "ਪਹਿਲਾਂ ਵਿਸ਼ਲੇਸ਼ਣ ਕਰੋ"
#     }
# }

# if "lang" not in st.session_state:
#     st.session_state.lang = "English"

# lang = LANGUAGES[st.session_state.lang]

# # ================= CSS =================
# st.markdown("""
# <style>
# .stApp {background: linear-gradient(135deg,#020403,#071a12); color:white;}
# .card {
#     background: rgba(255,255,255,0.05);
#     border-radius:20px;
#     padding:20px;
#     box-shadow:0 10px 30px rgba(0,0,0,0.5);
#     margin-bottom:15px;
# }
# .stButton>button {
#     background: linear-gradient(135deg,#ffcc33,#d4a017);
#     color:black;
#     font-weight:bold;
# }
# </style>
# """, unsafe_allow_html=True)

# # ================= SESSION =================
# if "chat_hist" not in st.session_state:
#     st.session_state.chat_hist = []

# # ================= NAVBAR =================
# col1, col2, col3 = st.columns([2,6,2])

# with col1:
#     st.markdown("### 🌱 AgriVision Pro")

# with col2:
#     nav = st.radio(
#         "",
#         [lang["dashboard"], lang["analysis"], lang["results"]],
#         horizontal=True
#     )

# with col3:
#     st.selectbox("🌐", list(LANGUAGES.keys()), key="lang")

# st.divider()

# # ================= CHATBOT =================
# with st.sidebar:
#     st.title("🤖 AI Assistant")

#     user_q = st.text_input("Ask anything...")

#     if user_q:
#         context = {}

#         if "soil" in st.session_state:
#             context["soil"] = st.session_state.soil
#         if "weather" in st.session_state:
#             context["weather"] = st.session_state.weather
#         if "final" in st.session_state:
#             context["crops"] = st.session_state.final

#         res = chatbot_reply(user_q, context=context)
#         st.session_state.chat_hist.append((user_q, res))

#     for q, a in st.session_state.chat_hist[-5:]:
#         st.write(f"🧑 {q}")
#         st.write(f"🤖 {a}")

# # ================= DASHBOARD =================
# if nav == lang["dashboard"]:

#     st.markdown("## 🚜 Farm Overview")

#     soil = st.session_state.get("soil", "Not Analyzed")
#     weather = st.session_state.get("weather", {})

#     weather_text = weather.get("description", "--") if isinstance(weather, dict) else "--"

#     col1, col2, col3 = st.columns(3)

#     col1.markdown(f'<div class="card">🌱 Soil<br><b>{soil}</b></div>', unsafe_allow_html=True)
#     col2.markdown(f'<div class="card">🌦 Weather<br><b>{weather_text}</b></div>', unsafe_allow_html=True)
#     col3.markdown('<div class="card">💰 Profit<br><b>Check Results</b></div>', unsafe_allow_html=True)

# # ================= ANALYSIS =================
# elif nav == lang["analysis"]:

#     st.markdown("## 🔬 Farm Analysis")

#     # ================= LOCATION =================
#     location = st.text_input(f"📍 {lang['location']}", "Ludhiana", key="location_input")

#     # ================= WEATHER =================
#     st.markdown("### 🌦 Weather")

#     if st.button("Get Weather", key="weather_btn"):

#         try:
#             weather = get_weather(location)

#             st.session_state["weather"] = weather
            

#             st.success("✅ Weather fetched")

#             st.write(f"📍 {weather['city']}")
#             st.write(f"🌡 {weather['temperature']} °C")
#             st.write(f"💧 {weather['humidity']} %")
#             st.write(f"🌧 {weather['rainfall']} mm")

#         except Exception as e:
#             st.error(f"Weather Error: {e}")

#     # ================= SOIL =================
#     st.markdown("### 🌱 Soil")

#     uploaded = st.file_uploader(lang["upload"], type=["jpg","png"], key="soil_upload")

#     if uploaded:
#         with open("temp.jpg","wb") as f:
#             f.write(uploaded.getbuffer())

#         st.image("temp.jpg", width=300)

#         if st.button("Analyze Soil", key="soil_btn"):

#             try:
#                 soil_result = predict_soil("temp.jpg")

#                 soil = soil_result["soil_type"]   # ✅ FIX
#                 soil = soil_result["soil_type"].lower()
#                 soil_data = get_soil_data(soil)

#                 if soil_data is None:
#                     st.error("Soil data not found. Try another image.")
#                     st.stop()


#                 st.session_state["soil"] = soil
#                 st.session_state["soil_data"] = soil_data
#                 st.session_state["soil_full"] = soil_result   # 🔥 extra info

#                 st.success(f"✅ Soil detected: {soil}")

#                 # 🔥 UI Upgrade
#                 st.markdown("### 🧪 Soil Insights")
#                 col1, col2, col3 = st.columns(3)

#                 col1.metric("💧 Moisture", soil_result["moisture"])
#                 col2.metric("🧱 Texture", soil_result["texture"])
#                 col3.metric("🌿 Organic", soil_result["organic_content"])
#                 st.markdown("### 🌾 Soil Nutrients (From Dataset)")

#                 col4, col5, col6, col7 = st.columns(4)

#                 col4.metric("N", round(soil_data["N"], 2))
#                 col5.metric("P", round(soil_data["P"], 2))
#                 col6.metric("K", round(soil_data["K"], 2))
#                 col7.metric("pH", round(soil_data["ph"], 2))

#             except Exception as e:
#                 st.error(f"Soil Error: {e}")
# # ================= RESULTS =================
# elif nav == lang["results"]:
#     if "weather" not in st.session_state or "soil_data" not in st.session_state:
#         st.warning("⚠️ Please run Analysis first")
#         st.stop()

#     st.markdown("## 🌾 Crop Intelligence")

#     if "soil_data" not in st.session_state:
#         st.warning(lang["warning"])

#     else:
#         with st.spinner("Generating crops..."):

#             crops = predict_crops(
#                 st.session_state["soil_data"],
#                 st.session_state["weather"]
# )

#             final = calculate_profit(crops, st.session_state["weather"])
#             st.session_state.final = final

#         cols = st.columns(3)
#         medals = ["🥇","🥈","🥉"]

#         for i, crop in enumerate(final[:3]):
#             cols[i].markdown(f"""
#             <div class="card">
#             <h2>{medals[i]}</h2>
#             <h3>{crop['crop']}</h3>
#             💰 ₹{crop['profit']}<br>
#             📊 {crop['confidence']}%
#             </div>
#             """, unsafe_allow_html=True)

#         st.subheader(lang["profit"])
#         st.bar_chart({c['crop']: c['profit'] for c in final[:3]})

#         # ================= AI INSIGHTS =================
#         st.markdown(f"### 🧠 {lang['insights']}")

#         best = final[0]

#         st.info(f"""
#         ✔ Best crop: {best['crop']}  
#         ✔ High profitability  
#         ✔ Confidence: {best['confidence']}%  
#         ✔ Suitable for current conditions  
#         """)
import streamlit as st
import time
import os

# --- CONFIG ---
st.set_page_config(page_title="AgriVision Pro", layout="wide", initial_sidebar_state="expanded")

# --- LANGUAGE DICTIONARY ---
LANG_DICT = {
    "English": {
        "title": "AGRIVISION PRO",
        "slogan": "Empowering Punjab's Agriculture",
        "nav": ["Home", "Land & Lab", "Nutrient View", "Crop Intelligence", "Action Report"],
        "login": "Secure Farmer Login",
        "acreage": "Enter Farm Acreage (Acres)",
        "upload": "Upload Soil Health Card",
        "scanning": "Scanning Document...",
        "next": "Next",
        "back": "Back",
        "top_crops": "Top 3 Recommended Crops",
        "sowing": "Optimal Sowing Time",
        "profit": "Market Profit Potential",
        "fertilizer": "Prescribed Fertilizer (Bags)",
        "advice": "Kisan Expert Advice",
        "tip": "Tip: Accurate acreage ensures precision fertilizer application!"
    },
    "हिंदी": {
        "title": "एग्रीविज़न प्रो",
        "slogan": "पंजाब की कृषि का सशक्तिकरण",
        "nav": ["होम", "भूमि और लैब", "पोषक तत्व", "फसल चयन", "एक्शन रिपोर्ट"],
        "login": "किसान लॉगिन",
        "acreage": "खेत का क्षेत्रफल (एकड़)",
        "upload": "मृदा कार्ड अपलोड करें",
        "scanning": "स्कैनिंग जारी है...",
        "next": "आगे",
        "back": "पीछे",
        "top_crops": "शीर्ष 3 अनुशंसित फसलें",
        "sowing": "बुआई का सही समय",
        "profit": "लाभ की संभावना",
        "fertilizer": "उर्वरक की आवश्यकता (बोरी)",
        "advice": "विशेषज्ञ सलाह",
        "tip": "सुझाव: सटीक क्षेत्रफल से सही खाद की मात्रा पता चलती है!"
    },
    "ਪੰਜਾਬੀ": {
        "title": "ਐਗਰੀਵਿਜ਼ਨ ਪ੍ਰੋ",
        "slogan": "ਪੰਜਾਬ ਦੀ ਖੇਤੀਬਾੜੀ ਦਾ ਸਸ਼ਕਤੀਕਰਨ",
        "nav": ["ਹੋਮ", "ਜ਼ਮੀਨ ਅਤੇ ਲੈਬ", "ਪੌਸ਼ਟਿਕ ਤੱਤ", "ਫਸਲ ਦੀ ਚੋਣ", "ਐਕਸ਼ਨ ਰਿਪੋਰਟ"],
        "login": "ਕਿਸਾਨ ਲੌਗਇਨ",
        "acreage": "ਖੇਤ ਦਾ ਰਕਬਾ (ਏਕੜ)",
        "upload": "ਮਿੱਟੀ ਕਾਰਡ ਅਪਲੋਡ ਕਰੋ",
        "scanning": "ਸਕੈਨ ਕੀਤਾ ਜਾ ਰਿਹਾ ਹੈ...",
        "next": "ਅੱਗੇ",
        "back": "ਪਿੱਛੇ",
        "top_crops": "ਚੋਟੀ ਦੀਆਂ 3 ਫਸਲਾਂ",
        "sowing": "ਬਿਜਾਈ ਦਾ ਸਮਾਂ",
        "profit": "ਮੁਨਾਫਾ ਪੱਧਰ",
        "fertilizer": "ਖਾਦ ਦੀ ਲੋੜ (ਬੋਰੀਆਂ)",
        "advice": "ਮਾਹਰ ਸਲਾਹ",
        "tip": "ਸੁਝਾਅ: ਜ਼ਮੀਨ ਦੇ ਰਕਬੇ ਨਾਲ ਖਾਦ ਦੀ ਸਹੀ ਮਾਤਰਾ ਪਤਾ ਲੱਗਦੀ ਹੈ!"
    }
}

# --- STATE MANAGEMENT ---
if 'slide' not in st.session_state:
    st.session_state.slide = 1
if 'acreage' not in st.session_state:
    st.session_state.acreage = 0.0

# --- IMPROVED CSS (Highlights & Backgrounds) ---
st.markdown(f"""
    <style>
    /* SIDEBAR STYLING */
    [data-testid="stSidebar"] {{
        background-color: #1B3F21;
        border-right: 2px solid #2ECC71;
    }}
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {{
        color: #FFFFFF !important;
    }}
    .stSidebar [data-testid="stButton"] button {{
        background-color: rgba(255,255,255,0.05);
        color: #FFFFFF;
        border: 1px solid rgba(46, 204, 113, 0.4);
        width: 100%;
        text-align: left;
    }}
    .stSidebar [data-testid="stButton"] button:hover {{
        background-color: #2ECC71;
        color: #1B3F21;
    }}

    /* HIGHLIGHT BOXES */
    .highlight-box {{
        background-color: #f0f9f1;
        padding: 15px;
        border-radius: 12px;
        border: 2px dashed #2ECC71;
        margin-bottom: 15px;
    }}

    /* HERO BACKGROUND */
    .login-hero {{
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1350&q=80');
        background-size: cover;
        background-position: center;
        padding: 80px 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }}

    /* CARD STYLING */
    .card {{
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        border-left: 10px solid #2ECC71;
        margin-bottom: 20px;
    }}

    /* MASCOT STYLING */
    .mascot-container {{ position: fixed; bottom: 20px; right: 20px; z-index: 1000; text-align: center; }}
    .mascot-img {{ width: 95px; height: 95px; border-radius: 50%; border: 4px solid #FFFFFF; box-shadow: 0 4px 15px rgba(0,0,0,0.4); background: white; object-fit: cover; }}
    .mascot-label {{ background: #1B3F21; color: white; font-size: 11px; border-radius: 10px; padding: 4px 12px; margin-top: 5px; font-weight: bold; border: 1px solid #2ECC71; }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
col_lang, col_logo = st.columns([1, 1])
with col_lang:
    lang = st.selectbox("🌐 Language", ["English", "हिंदी", "ਪੰਜਾਬੀ"])
    L = LANG_DICT[lang]
with col_logo:
    st.markdown('<div style="text-align:right;"><img src="https://cdn-icons-png.flaticon.com/512/892/892926.png" style="width:65px; border-radius:50%; border:3px solid #1B3F21; background:#f9f9f9; padding:5px;"></div>', unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown(f"<h1 style='font-size:26px;'>{L['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#2ECC71; font-weight:bold;'>{L['slogan']}</p>", unsafe_allow_html=True)
    st.divider()
    nav_icons = ['🏠','📍','🧪','🌾','📋']
    for i, name in enumerate(L['nav']):
        if st.button(f"{nav_icons[i]} {name}"):
            st.session_state.slide = i + 1
            st.rerun()

# --- SLIDE 1: HOME ---
if st.session_state.slide == 1:
    st.markdown(f'<div class="login-hero"><h1>{L["title"]}</h1><p>Smart Farming for a Sustainable Punjab</p></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="card"><h2>{L["login"]}</h2>', unsafe_allow_html=True)
    st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
    st.text_input("Farmer Mobile Number")
    st.text_input("Password", type="password")
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button(L['next']): st.session_state.slide = 2; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- SLIDE 2: LAND & LAB ---
elif st.session_state.slide == 2:
    if st.button(f"← {L['back']}"): st.session_state.slide = 1; st.rerun()
    st.markdown(f'<div class="card"><h3>{L["acreage"]}</h3>', unsafe_allow_html=True)
    st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
    st.session_state.acreage = st.number_input("", min_value=0.0, step=0.5, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    st.divider()
    st.write(f"**{L['upload']}**")
    st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    if uploaded_file:
        with st.spinner(L['scanning']):
            time.sleep(1.5)
            st.success("Analysis Complete!")
            if st.button(L['next']): st.session_state.slide = 3; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- SLIDE 3: NUTRIENT VIEW ---
elif st.session_state.slide == 3:
    if st.button(f"← {L['back']}"): st.session_state.slide = 2; st.rerun()
    st.markdown(f"<h2 style='text-align:center; color:#1B3F21;'>{L['nav'][2]}</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div style="display: flex; justify-content: center; align-items: flex-end; height: 320px; gap: 30px; margin-top: 20px;">
            <div style="text-align:center;"><div style="width:130px; height:130px; border:8px solid #e74c3c; border-radius:50%; display:flex; flex-direction:column; justify-content:center; background:rgba(231,76,60,0.05);"><b>40%</b><br><small>Nitrogen</small></div><span style="color:#e74c3c; font-weight:bold;">Low</span></div>
            <div style="text-align:center; transform: translateY(-70px);"><div style="width:170px; height:170px; border:10px solid #f39c12; border-radius:50%; display:flex; flex-direction:column; justify-content:center; background:rgba(243,156,18,0.1); box-shadow: 0 10px 20px rgba(243,156,18,0.2);"><b>15%</b><br><small>Phosphorus</small></div><span style="color:#f39c12; font-weight:bold;">Medium</span></div>
            <div style="text-align:center;"><div style="width:130px; height:130px; border:8px solid #2ecc71; border-radius:50%; display:flex; flex-direction:column; justify-content:center; background:rgba(46,204,113,0.05);"><b>85%</b><br><small>Potassium</small></div><span style="color:#2ecc71; font-weight:bold;">Optimal</span></div>
        </div>
        <div style="margin-top: 40px; text-align: center;">
            <div style="display: inline-block; padding: 15px 40px; border-radius: 50px; background: linear-gradient(90deg, #e74c3c, #f1c40f, #2ecc71, #3498db); color: white;">
                <span style="font-size: 18px; font-weight: bold;">Soil pH Value: <span style="font-size: 26px; background: white; color: #333; padding: 2px 12px; border-radius: 20px; margin-left: 10px;">6.8</span></span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    if st.button(L['next']): st.session_state.slide = 4; st.rerun()

# --- SLIDE 4: CROP INTELLIGENCE ---
elif st.session_state.slide == 4:
    if st.button(f"← {L['back']}"): st.session_state.slide = 3; st.rerun()
    st.header(L['top_crops'])
    c1, c2, c3 = st.columns(3)
    crops = [("Wheat", "🌾", "High"), ("Mustard", "🌼", "Medium"), ("Gram", "🌿", "High")]
    for i, (name, img, prf) in enumerate(crops):
        with [c1, c2, c3][i]:
            st.markdown(f'<div class="card" style="text-align:center;"><h1>{img}</h1><h3>{name}</h3><p>{L["profit"]}: {prf}</p></div>', unsafe_allow_html=True)
            if st.button(f"Select {name}", key=name): 
                st.session_state.selected_crop = name
                st.session_state.slide = 5; st.rerun()

# --- SLIDE 5: ACTION REPORT ---
elif st.session_state.slide == 5:
    if st.button(f"← {L['back']}"): st.session_state.slide = 4; st.rerun()
    st.markdown(f"<div class='card'><h2>Final Prescription: {st.session_state.get('selected_crop', 'Wheat')}</h2>", unsafe_allow_html=True)
    u_bags = round(st.session_state.acreage * 1.2, 1)
    d_bags = round(st.session_state.acreage * 0.7, 1)
    col_a, col_b = st.columns(2)
    with col_a:
        st.success(f"**{L['fertilizer']}:**")
        st.write(f"🧪 Urea: {u_bags} Bags")
        st.write(f"🧪 DAP: {d_bags} Bags")
    with col_b:
        st.warning(f"💡 **{L['advice']}:**")
        st.write("1. Split Nitrogen dose into three applications.")
        st.write("2. Apply DAP at sowing time.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- MASCOT ---
logo_path = "kisan_logo.png"
display_img = logo_path if os.path.exists(logo_path) else "https://cdn-icons-png.flaticon.com/512/1995/1995641.png"
st.markdown(f'''<div class="mascot-container"><img src="{display_img}" class="mascot-img"><div class="mascot-label">KISAN SAHAYAK AI</div></div>''', unsafe_allow_html=True)









