"""
Feature Transformation & Flood Risk Prediction
Transforms weather data to ML features and predicts flood risk
"""

import numpy as np
import pandas as pd
import joblib
import os
from datetime import datetime


def load_models():
    """Load trained ML models and scalers for all disasters"""
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ml_model', 'saved_models')

    models = {}
    scalers = {}

    # Define paths
    paths = {
        'flood': ('flood_model.pkl', 'scaler.pkl'),
        'cyclone': ('cyclone_model.pkl', 'cyclone_scaler.pkl'),
        'heatwave': ('heatwave_model.pkl', 'heatwave_scaler.pkl')
    }

    for disaster, (m_file, s_file) in paths.items():
        m_path = os.path.join(model_path, m_file)
        s_path = os.path.join(model_path, s_file)
        
        if os.path.exists(m_path) and os.path.exists(s_path):
            models[disaster] = joblib.load(m_path)
            scalers[disaster] = joblib.load(s_path)
    
    return models, scalers


def transform_to_features_flood(weather_data):
    """Transform weather API data to 10 ML model features for Flood"""

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

def transform_to_features_cyclone(weather_data):
    """Transform weather API data to ML model features for Cyclone"""
    
    wind_speed = weather_data['wind_speed'] * 1.5 # Gust estimate
    pressure = weather_data['pressure']
    
    # Estimate rainfall
    rainfall = weather_data['rainfall_1h'] * np.random.uniform(8, 15)
    if rainfall < 1 and pressure < 1000:
        rainfall = np.random.uniform(10, 80)
        
    distance_to_coast = np.random.uniform(10, 200) # Assuming coastal proxy
    system_movement_speed = np.random.uniform(10, 25)
    
    sea_surface_temp = weather_data['temperature'] + np.random.uniform(-2, 2)
    ocean_heat_content = np.random.uniform(30, 90)
    
    elevation = np.random.uniform(5, 50) # Mostly coastal
    
    return {
        'wind_speed': round(wind_speed, 2),
        'pressure': round(pressure, 2),
        'sea_surface_temp': round(sea_surface_temp, 2),
        'rainfall': round(rainfall, 2),
        'distance_to_coast': round(distance_to_coast, 2),
        'system_movement_speed': round(system_movement_speed, 2),
        'humidity': round(weather_data['humidity'], 2),
        'ocean_heat_content': round(ocean_heat_content, 2),
        'month': datetime.now().month,
        'elevation': round(elevation, 2)
    }

def transform_to_features_heatwave(weather_data):
    """Transform weather API data to ML model features for Heatwave"""
    
    max_temp = weather_data['temperature'] + np.random.uniform(0, 4)
    humidity = weather_data['humidity']
    
    heat_index = max_temp
    if max_temp >= 27 and humidity >= 40:
        heat_index = max_temp + (humidity - 40) * 0.1
        
    consecutive_hot_days = 0
    if max_temp > 35:
        consecutive_hot_days = np.random.randint(1, 5)
        
    soil_moisture = np.random.uniform(10, 40) # Assume drier during heatwave
    cloud_cover = weather_data.get('cloud_cover', np.random.uniform(0, 30))
    urban_heat_island_idx = np.random.uniform(5, 10)
    
    historical_avg_temp = 30 # Rough Indian summer avg
    temp_anomaly = max_temp - historical_avg_temp
    
    return {
        'max_temperature': round(max_temp, 2),
        'heat_index': round(heat_index, 2),
        'humidity': round(humidity, 2),
        'consecutive_hot_days': consecutive_hot_days,
        'wind_speed': round(weather_data['wind_speed'], 2),
        'soil_moisture': round(soil_moisture, 2),
        'month': datetime.now().month,
        'cloud_cover': round(cloud_cover, 2),
        'urban_heat_island_idx': round(urban_heat_island_idx, 2),
        'temp_anomaly': round(temp_anomaly, 2)
    }


def predict_risk(features, model, scaler, disaster_type, translations, lang='en'):
    """Predict risk level using trained ML model"""

    # Ensure correct column order matching training data
    feature_names = {
        'flood': ['rainfall', 'river_level', 'humidity', 'month', 'wind_speed',
                     'temperature', 'soil_moisture', 'elevation', 'drainage_density',
                     'land_use_index'],
        'cyclone': ['wind_speed', 'pressure', 'sea_surface_temp', 'rainfall',
                    'distance_to_coast', 'system_movement_speed', 'humidity',
                    'ocean_heat_content', 'month', 'elevation'],
        'heatwave': ['max_temperature', 'heat_index', 'humidity', 'consecutive_hot_days',
                     'wind_speed', 'soil_moisture', 'month', 'cloud_cover',
                     'urban_heat_island_idx', 'temp_anomaly']
    }
    
    cols = feature_names[disaster_type]
    features_df = pd.DataFrame([features])[cols]

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
