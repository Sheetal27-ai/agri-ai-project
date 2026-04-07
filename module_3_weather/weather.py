def get_weather(location):
    # dummy data (for now)
    return {
        "temperature": 28,
        "humidity": 70,
        "rainfall": 200
    }


# test
if __name__ == "__main__":
    data = get_weather("Punjab")
    print("Weather Data:", data)