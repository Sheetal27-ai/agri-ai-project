def calculate_profit(crops: list) -> list:
    """
    Takes top 3 crops from predict.py and adds profit data.

    Args:
        crops: list of dicts → [{"crop": "rice", "confidence": 87.5}, ...]

    Returns:
        list of dicts with profit added, sorted by profit descending
        [{"crop": "rice", "confidence": 87.5, "profit": 40500}, ...]
    """

    # Yield (quintals/hectare), Price (₹/quintal), Cost (₹/hectare)
    # All 22 crops from standard Kaggle crop recommendation dataset
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

        # extras from your original file
        "wheat":       {"yield": 30, "price": 2000, "cost": 20000},
        "sugarcane":   {"yield": 50, "price": 1500, "cost": 30000},
        "barley":      {"yield": 28, "price": 1700, "cost": 16000},
        "mustard":     {"yield": 18, "price": 4000, "cost": 15000},
    }

    results = []

    for item in crops:
        crop_name = item["crop"]
        confidence = item["confidence"]
        data = CROP_DATA.get(crop_name.lower())

        if data:
            profit = (data["yield"] * data["price"]) - data["cost"]
        else:
            # Crop not in table — still include it, profit unknown
            profit = None

        results.append({
            "crop":       crop_name,
            "confidence": confidence,
            "profit":     profit        # ₹ per hectare, None if unknown
        })

    # Sort by profit descending (put None at end)
    results.sort(key=lambda x: x["profit"] if x["profit"] is not None else -1, reverse=True)

    return results


# Test
if __name__ == "__main__":
    # Simulating output from predict.py
    crops = [
        {"crop": "muskmelon", "confidence": 49.0},
        {"crop": "coffee",    "confidence": 15.0},
        {"crop": "mothbeans", "confidence": 9.0}
    ]

    results = calculate_profit(crops)

    print("Final Ranked Crops (by profit):\n")
    for i, r in enumerate(results, 1):
        profit_str = f"₹{r['profit']:,}/hectare" if r["profit"] else "unknown"
        print(f"  {i}. {r['crop']:<12} | Confidence: {r['confidence']}% | Profit: {profit_str}")