import random

def predict_soil(image_path):
    classes = ["clay", "loamy", "sandy", "black"]
    return random.choice(classes)

# test
if __name__ == "__main__":
    result = predict_soil("test.jpg")
    print("Soil Type:", result)