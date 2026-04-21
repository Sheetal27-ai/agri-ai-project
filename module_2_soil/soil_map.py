import pandas as pd
import os
from utils.path_utils import get_path

# ================= LOAD DATASET =================
file_path = get_path("data", "data.csv")

if not os.path.exists(file_path):
    raise FileNotFoundError(f"❌ data.csv not found at {file_path}")

df = pd.read_csv(file_path)

# ================= CLEAN COLUMN NAMES =================
df.columns = [col.strip().lower() for col in df.columns]

# Expected columns (adjust if needed)
REQUIRED_COLUMNS = ["n", "p", "k", "ph"]

for col in REQUIRED_COLUMNS:
    if col not in df.columns:
        raise ValueError(f"❌ Column '{col}' not found in data.csv")


# ================= MAIN FUNCTION =================
def get_soil_data(soil_type):
    """
    Returns averaged soil nutrient values based on soil type.
    If soil_type column is not present, returns global average.
    """

    soil_type = soil_type.lower()

    # Create safe copy (IMPORTANT for stability)
    df_copy = df.copy()

    # ================= CASE 1: dataset has soil_type column =================
    if "soil_type" in df_copy.columns:

        df_copy["soil_type"] = df_copy["soil_type"].astype(str).str.lower()

        soil_rows = df_copy[df_copy["soil_type"] == soil_type]

        # fallback if no match
        if soil_rows.empty:
            soil_rows = df_copy[df_copy["soil_type"] == "loamy"]

        # final fallback
        if soil_rows.empty:
            soil_rows = df_copy

    # ================= CASE 2: no soil_type column =================
    else:
        soil_rows = df_copy


    # ================= COMPUTE AVERAGE =================
    soil_data = {
        "N": float(soil_rows["n"].mean()),
        "P": float(soil_rows["p"].mean()),
        "K": float(soil_rows["k"].mean()),
        "ph": float(soil_rows["ph"].mean())
    }

    return soil_data


# ================= TEST =================
if __name__ == "__main__":
    test_soil = "Loamy"
    data = get_soil_data(test_soil)
    print("Soil Data:", data)