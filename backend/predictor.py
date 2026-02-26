"""
Feature Transformation & Flood Risk Prediction
Transforms weather data to ML features and predicts flood risk
"""

import numpy as np
import pandas as pd
import joblib
import os
from datetime import datetime


def load_model():
    """Load trained ML model and scaler"""
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ml_model', 'saved_models')

    model_file = os.path.join(model_path, 'flood_model.pkl')
    scaler_file = os.path.join(model_path, 'scaler.pkl')

    if not os.path.exists(model_file) or not os.path.exists(scaler_file):
        return None, None

    model = joblib.load(model_file)
    scaler = joblib.load(scaler_file)
    return model, scaler


def transform_to_features(weather_data):
    """Transform weather API data to 10 ML model features"""

    # Estimate 24h rainfall from 1h data
    rainfall_1h = weather_data['rainfall_1h']
    rainfall_estimate = rainfall_1h * np.random.uniform(8, 15)

    # If no rain data, estimate from humidity and pressure
    if rainfall_estimate < 1:
        if weather_data['humidity'] > 85 and weather_data['pressure'] < 1005:
            rainfall_estimate = np.random.uniform(20, 50)

    humidity = weather_data['humidity']

    # Estimate river level
    river_level = 5.0 + (rainfall_estimate / 100) + np.random.uniform(-1, 2)
    river_level = max(0.0, river_level)

    current_month = datetime.now().month

    # Estimate soil moisture from humidity and rainfall
    soil_moisture = humidity * 0.4 + (rainfall_estimate / 5) + np.random.normal(0, 5)
    soil_moisture = max(0.0, min(100.0, soil_moisture))

    # Estimate elevation (reasonable default for Indian cities)
    elevation = np.random.uniform(50, 300)

    # Estimate drainage density
    drainage_density = np.random.uniform(3, 7)

    # Estimate land use index (urban default)
    land_use_index = np.random.uniform(5, 8)

    return {
        'rainfall': round(rainfall_estimate, 2),
        'river_level': round(river_level, 2),
        'humidity': round(humidity, 2),
        'month': current_month,
        'wind_speed': round(weather_data['wind_speed'], 2),
        'temperature': round(weather_data['temperature'], 2),
        'soil_moisture': round(soil_moisture, 2),
        'elevation': round(elevation, 2),
        'drainage_density': round(drainage_density, 2),
        'land_use_index': round(land_use_index, 2)
    }


def predict_flood_risk(features, model, scaler, translations, lang='en'):
    """Predict flood risk level using trained ML model"""

    # Ensure correct column order matching training data
    feature_names = ['rainfall', 'river_level', 'humidity', 'month', 'wind_speed',
                     'temperature', 'soil_moisture', 'elevation', 'drainage_density',
                     'land_use_index']
    features_df = pd.DataFrame([features])[feature_names]

    features_scaled = scaler.transform(features_df)

    risk_level = int(model.predict(features_scaled)[0])
    probabilities = model.predict_proba(features_scaled)[0]

    # Get translated labels
    tr = translations.get(lang, translations['en'])
    risk_info = tr['risk_labels'][risk_level]
    actions = tr['risk_actions'][risk_level]
    prob_labels = tr['prob_labels']

    color_map = {0: '#10b981', 1: '#f59e0b', 2: '#f97316', 3: '#ef4444'}
    gradient_map = {
        0: 'linear-gradient(135deg, #0f766e, #10b981)',
        1: 'linear-gradient(135deg, #d97706, #f59e0b)',
        2: 'linear-gradient(135deg, #ea580c, #f97316)',
        3: 'linear-gradient(135deg, #dc2626, #ef4444)'
    }
    emoji_map = {0: '✅', 1: '⚠️', 2: '🚨', 3: '🆘'}

    return {
        'risk_level': risk_level,
        'probability': float(probabilities[risk_level]),
        'all_probs': dict(zip(prob_labels, [float(p) for p in probabilities])),
        'label': risk_info['label'],
        'title': risk_info['title'],
        'message': risk_info['message'],
        'actions': actions,
        'color': color_map[risk_level],
        'gradient': gradient_map[risk_level],
        'emoji': emoji_map[risk_level]
    }


# Emergency resources data
EMERGENCY_RESOURCES = {
    'mumbai': {
        'hospitals': ['🏥 KEM Hospital - 022-24107000', '🏥 Lilavati Hospital - 022-26567891', '🏥 Hinduja Hospital - 022-24447000'],
        'shelters': ['🏠 BMC Schools (Multiple)', '🏠 Community Halls', '🏠 Sports Complexes']
    },
    'delhi': {
        'hospitals': ['🏥 AIIMS Delhi - 011-26588500', '🏥 Safdarjung Hospital - 011-26165060', '🏥 RML Hospital - 011-23365525'],
        'shelters': ['🏠 Government Schools', '🏠 Community Centers - Karol Bagh', '🏠 Sports Complex - Dwarka']
    },
    'chennai': {
        'hospitals': ['🏥 Apollo Hospital - 044-28296000', '🏥 Stanley Medical - 044-25281351', '🏥 Rajiv Gandhi Govt - 044-25912121'],
        'shelters': ['🏠 Corporation Schools', '🏠 Kalyana Mandapams', '🏠 Community Halls']
    },
    'kolkata': {
        'hospitals': ['🏥 SSKM Hospital - 033-22041000', '🏥 Medical College - 033-22413077', '🏥 Apollo Gleneagles - 033-23203040'],
        'shelters': ['🏠 Municipality Schools', '🏠 Relief Centers']
    },
    'bangalore': {
        'hospitals': ['🏥 Victoria Hospital - 080-26700301', '🏥 St Johns Hospital - 080-25532979', '🏥 Manipal Hospital - 080-25021000'],
        'shelters': ['🏠 Government Schools', '🏠 Community Halls']
    }
}
