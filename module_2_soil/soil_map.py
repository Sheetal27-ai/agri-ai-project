def get_soil_data(soil_type):
    soil_map = {
        "loamy": {"N": 80, "P": 40, "K": 40, "ph": 6.5},
        "clay": {"N": 60, "P": 35, "K": 35, "ph": 7.0},
        "sandy": {"N": 40, "P": 20, "K": 20, "ph": 6.0},
        "black": {"N": 90, "P": 50, "K": 50, "ph": 7.5}
    }

    return soil_map.get(soil_type, None)


# test
if __name__ == "__main__":
    soil = "loamy"
    data = get_soil_data(soil)
    print("Soil Data:", data)