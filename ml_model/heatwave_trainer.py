import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

print("="*70)
print("  HEATWAVE RISK PREDICTION MODEL TRAINER")
print("="*70)

# ============================================================================
# STEP 1: GENERATE SYNTHETIC TRAINING DATA
# ============================================================================

print("\n[STEP 1] Generating synthetic heatwave data...")

np.random.seed(42)
n_samples = 2000

data = []

for i in range(n_samples):
    # Features for Heatwave Prediction
    
    month = np.random.randint(1, 13)
    is_summer = month in [4, 5, 6, 7]
    
    # Max Temperature (Celsius)
    max_temperature = np.random.uniform(25, 45)
    if is_summer:
        max_temperature += np.random.uniform(5, 8)
        
    # Humidity (%)
    humidity = np.random.uniform(10, 90)
    
    # Heat Index (Feels like temperature)
    # Simple estimation: if high temp and high humidity, feels much hotter
    if max_temperature >= 27 and humidity >= 40:
        heat_index = max_temperature + (humidity - 40) * 0.1
    else:
        heat_index = max_temperature
        
    heat_index += np.random.normal(0, 1)
    
    # Consecutive Hot Days
    if max_temperature > 35:
        consecutive_hot_days = np.random.randint(1, 15)
    else:
        consecutive_hot_days = 0
        
    # Wind Speed (km/h) - Dry hot winds (Loo) increase risk
    wind_speed = np.random.uniform(0, 40)
    
    # Soil Moisture (%) - Dry soil leads to higher sensible heat
    soil_moisture = np.random.uniform(5, 80)
    if is_summer:
        soil_moisture = max(0, soil_moisture - 20)
        
    # Cloud Cover (%) - Less clouds = more solar radiation
    cloud_cover = np.random.uniform(0, 100)
    if max_temperature > 38:
        cloud_cover = min(100, cloud_cover * 0.5)
        
    # Urban Heat Island Index (1-10)
    urban_heat_island_idx = np.random.uniform(1, 10)
    
    # Historical Avg Temp for that month
    historical_avg_temp = 25 + (10 if is_summer else 0) + np.random.normal(0, 2)
    
    # Temp Anomaly
    temp_anomaly = max_temperature - historical_avg_temp

    # Risk Calculation (Rule-based for synthetic data)
    risk_score = 0
    
    if max_temperature > 45: risk_score += 8
    elif max_temperature > 40: risk_score += 5
    elif max_temperature > 37: risk_score += 3
    
    if heat_index > 48: risk_score += 4
    elif heat_index > 41: risk_score += 2
    
    if consecutive_hot_days > 5: risk_score += 3
    elif consecutive_hot_days > 2: risk_score += 1
    
    if temp_anomaly > 6: risk_score += 3
    elif temp_anomaly > 4: risk_score += 1
    
    if is_summer: risk_score += 1
    
    if urban_heat_island_idx > 8: risk_score += 1
    if soil_moisture < 20: risk_score += 1
    
    if risk_score >= 12: risk_level = 3  # Critical / Extreme Heatwave
    elif risk_score >= 8: risk_level = 2   # High Risk / Severe Heatwave
    elif risk_score >= 4: risk_level = 1   # Warning / Heatwave
    else: risk_level = 0                   # Safe / Normal
    
    data.append({
        'max_temperature': round(max_temperature, 2),
        'heat_index': round(heat_index, 2),
        'humidity': round(humidity, 2),
        'consecutive_hot_days': consecutive_hot_days,
        'wind_speed': round(wind_speed, 2),
        'soil_moisture': round(soil_moisture, 2),
        'month': month,
        'cloud_cover': round(cloud_cover, 2),
        'urban_heat_island_idx': round(urban_heat_island_idx, 2),
        'temp_anomaly': round(temp_anomaly, 2),
        'risk_level': risk_level
    })

df = pd.DataFrame(data)

os.makedirs('data', exist_ok=True)
df.to_csv('data/heatwave_data.csv', index=False)

print(f"✅ Generated {len(df)} samples")
print(f"✅ Saved to: data/heatwave_data.csv")

# ============================================================================
# STEP 2: PREPARE DATA FOR TRAINING
# ============================================================================

X = df.drop('risk_level', axis=1)
y = df['risk_level']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ============================================================================
# STEP 3: TRAIN RANDOM FOREST MODEL
# ============================================================================

model = RandomForestClassifier(n_estimators=100, max_depth=15, min_samples_split=5, random_state=42, n_jobs=-1)
model.fit(X_train_scaled, y_train)

# ============================================================================
# STEP 4: EVALUATE MODEL
# ============================================================================

y_train_pred = model.predict(X_train_scaled)
y_test_pred = model.predict(X_test_scaled)
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

print(f"\nTraining Accuracy:   {train_accuracy*100:.2f}%")
print(f"Testing Accuracy:    {test_accuracy*100:.2f}%")

# ============================================================================
# STEP 5: SAVE MODEL AND SCALER
# ============================================================================

os.makedirs('models', exist_ok=True)
os.makedirs('saved_models', exist_ok=True)

joblib.dump(model, 'saved_models/heatwave_model.pkl')
joblib.dump(scaler, 'saved_models/heatwave_scaler.pkl')

print("\n✅ Heatwave Model and Scaler saved in saved_models/")
