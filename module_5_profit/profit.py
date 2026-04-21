def _generate_insight(crop_name, weather):
    """
    Generate simple AI insight based on weather
    """
    if not weather:
        return "Suitable under average conditions"

    temp = weather.get("temperature", 25)
    rain = weather.get("rainfall", 100)

    if crop_name in ["rice", "banana"] and rain > 150:
        return "High rainfall favors this crop 🌧"
    elif crop_name in ["wheat", "chickpea"] and temp < 25:
        return "Cool temperature is beneficial ❄"
    elif crop_name in ["cotton", "maize"] and temp > 30:
        return "Warm climate is ideal ☀"
    else:
        return "Moderately suitable conditions"


def calculate_profit(crops: list, weather_data=None) -> list:
    """
    Adds profit + insights to predicted crops

    Args:
        crops: list → [{"crop": "rice", "confidence": 87.5}, ...]
        weather_data: dict (optional)

    Returns:
        list → [{"crop": ..., "confidence": ..., "profit": ..., "insight": ...}]
    """

    # ================= CROP DATABASE =================
    CROP_DATA = {
        "rice":        {"yield": 25, "price": 2500, "cost": 22000},
        "maize":       {"yield": 35, "price": 1800, "cost": 18000},
        "chickpea":    {"yield": 12, "price": 5000, "cost": 18000},
        "kidneybeans": {"yield": 15, "price": 4500, "cost": 20000},
        "pigeonpeas":  {"yield": 10, "price": 5500, "cost": 17000},
        "mothbeans":   {"yield": 8,  "price": 6000, "cost": 15000},
        "mungbean":    {"yield": 10, "price": 5500, "cost": 16000},
        "blackgram":   {"yield": 9,  "price": 5800, "cost": 16000},
        "lentil":      {"yield": 12, "price": 5200, "cost": 17000},
        "pomegranate": {"yield": 20, "price": 8000, "cost": 40000},
        "banana":      {"yield": 60, "price": 1500, "cost": 35000},
        "mango":       {"yield": 15, "price": 7000, "cost": 30000},
        "grapes":      {"yield": 25, "price": 6000, "cost": 45000},
        "watermelon":  {"yield": 80, "price": 800,  "cost": 25000},
        "muskmelon":   {"yield": 60, "price": 1000, "cost": 20000},
        "apple":       {"yield": 20, "price": 9000, "cost": 50000},
        "orange":      {"yield": 25, "price": 4000, "cost": 30000},
        "papaya":      {"yield": 50, "price": 1500, "cost": 25000},
        "coconut":     {"yield": 30, "price": 3000, "cost": 20000},
        "cotton":      {"yield": 20, "price": 3000, "cost": 25000},
        "jute":        {"yield": 15, "price": 3500, "cost": 20000},
        "coffee":      {"yield": 10, "price": 6000, "cost": 30000},

        # extras
        "wheat":       {"yield": 30, "price": 2000, "cost": 20000},
        "sugarcane":   {"yield": 50, "price": 1500, "cost": 30000},
        "barley":      {"yield": 28, "price": 1700, "cost": 16000},
        "mustard":     {"yield": 18, "price": 4000, "cost": 15000},
    }

    results = []

    # ================= MAIN LOOP =================
    for item in crops:
        crop_name = item["crop"].lower()
        confidence = item.get("confidence", 0)

        data = CROP_DATA.get(crop_name)

        if data:
            profit = (data["yield"] * data["price"]) - data["cost"]
        else:
            profit = None

        insight = _generate_insight(crop_name, weather_data)

        results.append({
            "crop": crop_name,
            "confidence": confidence,
            "profit": profit,
            "insight": insight
    })

    # ================= SORT =================
    results.sort(
        key=lambda x: x["profit"] if x["profit"] is not None else -1,
        reverse=True
    )

    return results


# ================= TEST =================
if __name__ == "__main__":
    sample_crops = [
        {"crop": "rice", "confidence": 80},
        {"crop": "maize", "confidence": 60},
        {"crop": "coffee", "confidence": 40}
    ]

    sample_weather = {
        "temperature": 32,
        "humidity": 70,
        "rainfall": 200
    }

    output = calculate_profit(sample_crops, sample_weather)

    print("\n🌾 Final Results:\n")
    for i, r in enumerate(output, 1):
        profit_str = f"₹{r['profit']:,}" if r["profit"] else "Unknown"
        print(f"{i}. {r['crop']} | Profit: {profit_str} | {r['insight']}")