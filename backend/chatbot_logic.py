
# Mock dataset reflecting the current state of the farm
project_data = {
    "soil_type": "Loamy",
    "moisture": "22%",
    "ph": 6.8,
    "N": 85,
    "P": 42,
    "K": 15,
    "temperature": 31,
    "humidity": 44,
    "recommended_crop": "Wheat",
    "yield": 24.8,
    "profit": 48200
}

def get_chatbot_response(user_msg):
    msg = user_msg.lower().strip()

    # --- GENERAL QUESTIONS ---
    if "npk" in msg:
        return "NPK stands for Nitrogen (N), Phosphorus (P), and Potassium (K)—the three primary nutrients in commercial fertilizers. Each nutrient plays a key role: N for leaf growth, P for root/fruit development, and K for overall plant health."
    
    if "ph" in msg:
        return "pH scale measures how acidic or alkaline the soil is (0 to 14). Most crops grow best in slightly acidic to neutral soil (6.0 to 7.5)."
    
    if "soil type" in msg:
        return "Soil type refers to the composition of sand, silt, and clay in your soil. Common types include Sandy, Loamy, and Clay."
    
    if "crop prediction" in msg:
        return "Our system uses Machine Learning (Random Forest) to predict the best crops based on your soil health and local weather conditions."

    # --- PROJECT-SPECIFIC QUESTIONS ---
    if "which crop" in msg or "recommend" in msg:
        return f"Based on your {project_data['soil_type']} soil, {project_data['recommended_crop']} is highly recommended for maximum success."

    if "why" in msg and "wheat" in msg:
        return f"Wheat is recommended because your soil has a pH of {project_data['ph']} and moderate NPK levels, which perfectly suit wheat's growth cycle in {project_data['temperature']}°C weather."

    if "soil condition" in msg or "my soil" in msg:
        return f"Your soil is {project_data['soil_type']} with {project_data['moisture']} moisture. Nutrient levels are: N={project_data['N']}, P={project_data['P']}, K={project_data['K']}."

    if "cotton" in msg:
        return "Your current soil moisture and loamy type are okay for cotton, but wheat or maize might yield better profits currently."

    if "potassium" in msg or "k" in msg == "k":
        return f"Potassium (K) is crucial for water regulation and disease resistance. Your soil currently has {project_data['K']} units of Potassium."

    if "yield" in msg:
        return f"The estimated yield for {project_data['recommended_crop']} on your land is {project_data['yield']} quintals per acre."

    if "profit" in msg:
        return f"Your estimated profit for this season is ₹{project_data['profit']:,}."

    # --- FALLBACK ---
    return "I can help with soil, crops, weather, and profit predictions. Could you please rephrase your question?"
