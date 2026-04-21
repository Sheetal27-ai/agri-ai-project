def chatbot_reply(user_input):
    user_input = user_input.lower()

    # 🧭 Navigation help
    if "start" in user_input or "how to use" in user_input:
        return "Start by uploading soil data or image, then go to crop recommendation section."

    # 🌱 Soil health card
    if "soil health card" in user_input:
        return (
            "Soil Health Card is a government report that tells soil nutrients like NPK, pH, and helps choose crops."
        )

    # 🌾 Crop related
    if "crop" in user_input:
        return "Go to Crop Recommendation section to get best crop suggestion based on your soil."

    # 🌦️ Weather
    if "weather" in user_input:
        return "Weather module shows rainfall, temperature, and humidity for your location."

    # 💰 Profit
    if "profit" in user_input:
        return "Profit module calculates expected earnings from selected crop."

    # ❌ Default response
    return "I didn’t understand. Ask about soil, crop, weather, or profit."