# 🌾 Smart Crop Recommendation System

## 📌 Overview

This project is an AI-powered agricultural decision support system that helps farmers make data-driven decisions using **soil health, weather conditions, and location data**.

The system provides:

* 🌱 Crop recommendation
* 🧪 Fertilizer suggestions
* ⏱️ Optimal sowing time
* 📄 Soil Health Card (PDF/Image) analysis
* Market Analysis


## 🎯 Problem Statement

Farmers often struggle with:

* Selecting the right crop
* Understanding soil nutrient deficiencies
* Deciding sowing time based on weather

This leads to reduced productivity and profit. Our system solves this using **Machine Learning + Rule-based intelligence**.

---

## 🚀 Features

* 📊 Crop prediction using ML model
* 🌦️ Real-time weather integration
* 🧪 Fertilizer recommendation (based on soil deficiency)
* ⏰ Sowing time suggestion
* 📄 Document upload (Soil Health Card support)
* 🌍 Location-based recommendations

---

## 🧠 System Architecture

```
User Input / Document Upload
            ↓
   Text Extraction (OCR / PDF)
            ↓
     Soil Data Extraction
            ↓
     Weather API Integration
            ↓
     Crop Prediction Model
            ↓
   ┌────────────┴────────────┐
   ↓                         ↓
Fertilizer Module     Sowing Time Module
   ↓                         ↓
        Final Recommendations
```

---

## 📂 Project Structure

```
agri-project/
│── app.py                  # Main Streamlit application
│
├── module_1_image/         # Soil image analysis (if used)
│   └── predict.py
│
├── module_2_soil/          # Soil data extraction
│   └── soil_map.py
│
├── module_3_weather/       # Weather API integration
│   └── weather.py
│
├── module_4_crop/          # Crop prediction model
│   └── model.py
│
├── module_5_profit/        # Profit calculation (optional)
│   └── profit.py
│
├── utils/                  # Helper functions
│
├── data/                   # Dataset files
│
└── requirements.txt
```

---

## ⚙️ Tech Stack

### 🖥️ Frontend

* Streamlit / HTML, CSS, JavaScript

### 🧠 Backend

* Python

### 🤖 Machine Learning

* Scikit-learn
* XGBoost

### 📊 Data Processing

* Pandas, NumPy

### 🌦️ APIs

* Weather API

### 📄 Document Processing

* Tesseract OCR
* PyPDF2 / pdfplumber

---

## 📥 Input Parameters

### Soil Data:

* Nitrogen (N)
* Phosphorus (P)
* Potassium (K)
* pH
* Organic Carbon (optional)

### Weather Data:

* Temperature
* Humidity
* Rainfall

### Location:

* District / GPS

### Additional:

* Land Area (hectare/acre/bigha)

---

## 📤 Output

* ✅ Recommended Crop
* 🧪 Fertilizer Dose (kg/hectare)
* 📏 Total Fertilizer Required
* ⏱️ Best Sowing Time

---

## 🧠 Machine Learning Model

* Type: Supervised Learning
* Algorithms:

  * Random Forest
  * XGBoost (preferred)

The model is trained on historical agricultural datasets to learn relationships between **soil, weather, and crop suitability**.

---

## 🧪 Fertilizer Recommendation Logic

The system uses a **rule-based approach**:

* Compares soil nutrients with ideal crop requirements
* Suggests fertilizers to correct deficiencies

### Example:

```
If Nitrogen is low → Suggest Urea  
If Phosphorus is low → Suggest DAP  
If Potassium is low → Suggest MOP  
```

---

## 📏 Fertilizer Quantity Calculation

Fertilizer recommendations are generated **per hectare**.

### Formula:

```
Total Fertilizer = Dose per hectare × Land Area
```

### Example:

```
Urea: 120 kg/hectare  
Land Area: 2 hectares  

Total Urea = 120 × 2 = 240 kg
```

### ⚠️ Important:

* Land size is **NOT used in model training**
* It is only used for **final quantity calculation**
* Fertilizer depends on **soil condition, not farm size**

---

## ⏱️ Sowing Time Logic

Based on:

* Crop type
* Season (Kharif / Rabi)
* Weather conditions

### Example:

* Rice → June–July
* Wheat → October–November

---

## 📄 Document Processing (Soil Health Card)

Steps:

1. Upload document (PDF/Image)
2. Extract text using OCR/PDF parser
3. Parse values (N, P, K, pH)
4. Feed into ML model

---

## 📦 Installation

```
git clone https://github.com/your-username/agri-project.git
cd agri-project
pip install -r requirements.txt
```

---

## ▶️ Usage

```
streamlit run app.py
```

---

## 📊 Future Enhancements

* 📈 Crop yield prediction
* 💰 Profit estimation using mandi data
* 📱 Mobile app integration
* 🌍 Multi-language support

---

## 🤝 Contribution

Contributions are welcome! Feel free to fork the repo and submit pull requests.

---

## 📜 License

This project is for educational and research purposes.

---

## 👩‍💻 Author

Sheetal

