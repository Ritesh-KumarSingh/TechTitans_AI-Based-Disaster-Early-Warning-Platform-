import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

print("="*70)
print("  CYCLONE RISK PREDICTION MODEL TRAINER")
print("="*70)

# ============================================================================
# STEP 1: GENERATE SYNTHETIC TRAINING DATA
# ============================================================================

print("\n[STEP 1] Generating synthetic cyclone data...")

np.random.seed(42)
n_samples = 2000

data = []

for i in range(n_samples):
    # Features for Cyclone Prediction
    
    # Wind Speed (km/h) - Primary indicator
    wind_speed = np.random.exponential(30) + np.random.uniform(10, 200)
    
    # Sea Level Pressure (hPa) - Inverse relationship with intensity
    pressure = np.random.uniform(940, 1015)
    if wind_speed > 120:
        pressure -= np.random.uniform(20, 40)
        
    # Sea Surface Temperature (Celsius) - Fuel for cyclone (>26.5 is favorable)
    sea_surface_temp = np.random.uniform(24, 32)
    
    # Rainfall (mm) - Accompanying hazard
    rainfall = np.random.exponential(50) + np.random.uniform(0, 300)
    if wind_speed > 90:
        rainfall += np.random.uniform(50, 150)
        
    # Distance to Coast (km) - Risk decreases inland
    distance_to_coast = np.random.uniform(0, 500)
    
    # System Movement Speed (km/h) - Slower systems dump more rain
    system_movement_speed = np.random.uniform(5, 30)
    
    # Humidity (%) - Moisture available
    humidity = np.random.uniform(60, 100)
    if rainfall > 100:
        humidity = np.random.uniform(85, 100)
        
    # Ocean Heat Content (KJ/cm2) - Deep warm water
    ocean_heat_content = np.random.uniform(20, 120)
    
    # Month (1-12) - Cyclone seasons (Pre and Post monsoon in India: April-May, Oct-Dec)
    month = np.random.randint(1, 13)
    is_cyclone_season = month in [4, 5, 10, 11, 12]
    
    # Elevation (meters above sea level) - Surge impact
    elevation = np.random.exponential(50) + np.random.uniform(0, 200)
    
    # Adjust values for season
    if is_cyclone_season:
        sea_surface_temp += 1
        wind_speed += 20
        ocean_heat_content += 10

    # Risk Calculation (Rule-based for synthetic data)
    risk_score = 0
    
    if wind_speed > 180: risk_score += 8       # Super Cyclonic Storm
    elif wind_speed > 120: risk_score += 6     # Very Severe
    elif wind_speed > 90: risk_score += 4      # Severe
    elif wind_speed > 60: risk_score += 2      # Cyclonic Storm
    
    if pressure < 960: risk_score += 3
    elif pressure < 980: risk_score += 1
    
    if sea_surface_temp > 28: risk_score += 2
    
    if distance_to_coast < 50: risk_score += 3
    elif distance_to_coast < 150: risk_score += 1
    
    if ocean_heat_content > 80: risk_score += 2
    
    if is_cyclone_season: risk_score += 1
    
    # Distance mitigates wind speed over land
    if distance_to_coast > 200 and wind_speed > 100:
        risk_score -= 2
        
    # Surge risk
    if elevation < 10 and wind_speed > 90:
        risk_score += 2
    
    # Map risk score 
    if risk_score >= 12: risk_level = 3  # Critical
    elif risk_score >= 8: risk_level = 2   # High Risk
    elif risk_score >= 4: risk_level = 1   # Warning
    else: risk_level = 0                   # Safe
    
    data.append({
        'wind_speed': round(wind_speed, 2),
        'pressure': round(pressure, 2),
        'sea_surface_temp': round(sea_surface_temp, 2),
        'rainfall': round(rainfall, 2),
        'distance_to_coast': round(distance_to_coast, 2),
        'system_movement_speed': round(system_movement_speed, 2),
        'humidity': round(humidity, 2),
        'ocean_heat_content': round(ocean_heat_content, 2),
        'month': month,
        'elevation': round(elevation, 2),
        'risk_level': risk_level
    })

df = pd.DataFrame(data)

os.makedirs('data', exist_ok=True)
df.to_csv('data/cyclone_data.csv', index=False)

print(f"✅ Generated {len(df)} samples")
print(f"✅ Saved to: data/cyclone_data.csv")

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
os.makedirs('saved_models', exist_ok=True) # Ensure within ml_model folder this exists if run locally

joblib.dump(model, 'saved_models/cyclone_model.pkl')
joblib.dump(scaler, 'saved_models/cyclone_scaler.pkl')

print("\n✅ Cyclone Model and Scaler saved in saved_models/")
