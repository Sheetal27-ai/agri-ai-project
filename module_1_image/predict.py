import numpy as np
import cv2

def predict_soil(image_input):
    """
    Predict soil properties from image.

    Parameters:
        image_input (str or bytes): image path or bytes

    Returns:
        dict:
            {
                "soil_type": str,
                "moisture": str,
                "texture": str,
                "organic_content": str
            }
    """

    # ================= READ IMAGE =================
    if isinstance(image_input, str):
        image = cv2.imread(image_input)
    elif isinstance(image_input, bytes):
        nparr = np.frombuffer(image_input, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    else:
        raise ValueError("Invalid image input")

    if image is None:
        raise ValueError("Image could not be loaded")

    # ================= PREPROCESS =================
    image = cv2.resize(image, (256, 256))  # standard size

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    h, s, v = cv2.split(hsv)

    mean_brightness = np.mean(v)
    mean_hue = np.mean(h)
    mean_sat = np.mean(s)

    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.sum(edges / 255.0) / (edges.shape[0] * edges.shape[1])

    # ================= FEATURE LOGIC =================

    # Texture
    if edge_density > 0.08:
        texture = "Coarse"
    elif edge_density > 0.03:
        texture = "Medium"
    else:
        texture = "Fine"

    # Moisture
    if mean_brightness < 80:
        moisture = "High"
    elif mean_brightness < 150:
        moisture = "Medium"
    else:
        moisture = "Low"

    # Organic Content
    if mean_brightness < 70:
        organic_content = "High"
    elif mean_brightness < 130:
        organic_content = "Medium"
    else:
        organic_content = "Low"

    # Soil Type
    if mean_sat < 40 and edge_density > 0.05:
        soil_type = "Rocky"
    elif mean_hue < 20 and mean_sat > 100:
        soil_type = "Sandy"
    elif 20 <= mean_hue < 40 and mean_sat > 80:
        soil_type = "Clay"
    elif mean_brightness < 100:
        soil_type = "Alluvial"
    else:
        soil_type = "Loamy"

    # ================= RETURN =================
    return {
        "soil_type": soil_type,
        "moisture": moisture,
        "texture": texture,
        "organic_content": organic_content
    }


# BACKWARD COMPATIBILITY
process_image = predict_soil