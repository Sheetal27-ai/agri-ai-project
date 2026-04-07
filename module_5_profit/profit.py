def calculate_profit(crops):
    
    # dummy data (per hectare)
    crop_data = {
    "wheat": {"yield": 30, "price": 2000, "cost": 20000},
    "rice": {"yield": 25, "price": 2500, "cost": 22000},
    "maize": {"yield": 35, "price": 1800, "cost": 18000},
    "cotton": {"yield": 20, "price": 3000, "cost": 25000},
    "sugarcane": {"yield": 50, "price": 1500, "cost": 30000},
    "barley": {"yield": 28, "price": 1700, "cost": 16000},
    "mustard": {"yield": 18, "price": 4000, "cost": 15000},

    # 👉 ADD THESE
    "coffee": {"yield": 10, "price": 6000, "cost": 30000},
    "jute": {"yield": 15, "price": 3500, "cost": 20000}
}

    results = {}

    for crop in crops:
        data = crop_data.get(crop)

        if data:
            profit = (data["yield"] * data["price"]) - data["cost"]
            results[crop] = profit

    return results


def rank_crops(profit_dict):
    sorted_crops = sorted(profit_dict, key=profit_dict.get, reverse=True)
    return sorted_crops[:3]


# test
if __name__ == "__main__":
    crops = ["wheat", "rice", "maize"]
    
    profits = calculate_profit(crops)
    print("Profits:", profits)

    top = rank_crops(profits)
    print("Top Crops:", top)