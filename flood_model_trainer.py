"""
Flood Risk Prediction Model Trainer
Generates synthetic data and trains Random Forest classifier
For 10-hour hackathon MVP
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

print("="*70)
print("  FLOOD RISK PREDICTION MODEL TRAINER")
print("="*70)

# ============================================================================
# STEP 1: GENERATE SYNTHETIC TRAINING DATA
# ============================================================================

print("\n[STEP 1] Generating synthetic flood data...")

np.random.seed(42)
n_samples = 2000

data = []

for i in range(n_samples):
    # Generate realistic features
    
    # Rainfall (mm) - most important factor (45%)
    # Normal rain: 0-50mm, Heavy: 50-150mm, Extreme: 150+mm
    rainfall = np.random.exponential(50) + np.random.uniform(0, 150)
    
    # Humidity (%) - Indicates saturation (11%)
    humidity = 50 + (rainfall / 5) + np.random.uniform(0, 30)
    humidity = min(100, humidity)
    
    # River level (meters) - Second most important (32%)
    base_river = np.random.uniform(3, 7)
    river_level = base_river + (rainfall / 100) + np.random.uniform(-2, 5)
    river_level = max(0, river_level)
    
    # Temperature (Celsius) - Affects evaporation (3%)
    temperature = 25 + np.random.normal(0, 5)
    
    # Wind speed (km/h) - Storm indicator (3%)
    wind_speed = np.random.exponential(10) + np.random.uniform(5, 30)
    
    # Month (1-12) - Monsoon season matters (6%)
    month = np.random.randint(1, 13)
    is_monsoon = month in [6, 7, 8, 9]
    
    # NEW FEATURES
    # Soil Moisture (0-100%) - Saturated soil means runoff
    soil_moisture = humidity * 0.4 + (rainfall / 5) + np.random.normal(0, 10)
    soil_moisture = max(0, min(100, soil_moisture))
    
    # Elevation (meters above sea level) - Lower means higher risk
    elevation = np.random.exponential(100) + np.random.uniform(0, 500)
    
    # Drainage Density (Scale 1-10) - Lower density means less capacity to drain water
    drainage_density = np.random.uniform(1, 10)
    
    # Land Use Index (Scale 1-10) - 10=Urban (more runoff), 1=Forest (more absorption)
    land_use_index = np.random.uniform(1, 10)
    
    # Adjust values for monsoon season
    if is_monsoon:
        rainfall *= 1.5
        humidity += 10
        river_level += 1
        soil_moisture += 15
    
    # ========================================================================
    # RISK LEVEL CALCULATION (Rule-based for training data)
    # ========================================================================
    
    risk_score = 0
    
    # Rainfall contribution (Highest Weight ~45%)
    if rainfall > 200:
        risk_score += 8
    elif rainfall > 150:
        risk_score += 6
    elif rainfall > 80:
        risk_score += 4
    elif rainfall > 40:
        risk_score += 2
        
    # River level contribution (~32%)
    if river_level > 12:
        risk_score += 6
    elif river_level > 10:
        risk_score += 4
    elif river_level > 7:
        risk_score += 2
    elif river_level > 5:
        risk_score += 1
        
    # Humidity contribution (~11%)
    if humidity > 90:
        risk_score += 2
    elif humidity > 80:
        risk_score += 1
        
    # Add new features to risk score
    if soil_moisture > 85:
        risk_score += 2
    elif soil_moisture > 70:
        risk_score += 1
        
    if elevation < 50:
        risk_score += 2  # Low elevation = high risk
        
    if drainage_density < 3:
        risk_score += 1  # Poor drainage
        
    if land_use_index > 8:
        risk_score += 1  # High urban density
        
    # Monsoon season adds risk (6%)
    if is_monsoon:
        risk_score += 1
    
    # Small random factor for temp and wind (capturing the 3% weights indirectly)
    if wind_speed > 60:
        risk_score += 1
    
    # Map risk score to 4-level classification (Adjusted thresholds for higher max score)
    if risk_score >= 15:
        risk_level = 3  # Critical
    elif risk_score >= 10:
        risk_level = 2  # High Risk
    elif risk_score >= 5:
        risk_level = 1  # Warning
    else:
        risk_level = 0  # Safe
    
    # Store sample
    data.append({
        'rainfall': round(rainfall, 2),
        'river_level': round(river_level, 2),
        'humidity': round(humidity, 2),
        'month': month,
        'wind_speed': round(wind_speed, 2),
        'temperature': round(temperature, 2),
        'soil_moisture': round(soil_moisture, 2),
        'elevation': round(elevation, 2),
        'drainage_density': round(drainage_density, 2),
        'land_use_index': round(land_use_index, 2),
        'risk_level': risk_level
    })

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
os.makedirs('data', exist_ok=True)
df.to_csv('data/flood_data.csv', index=False)

print(f"✅ Generated {len(df)} samples")
print(f"✅ Saved to: data/flood_data.csv")
print(f"\nRisk Level Distribution:")
print(df['risk_level'].value_counts().sort_index())
print(f"\n   0 = Safe, 1 = Warning, 2 = High Risk, 3 = Critical")

# ============================================================================
# STEP 2: PREPARE DATA FOR TRAINING
# ============================================================================

print("\n[STEP 2] Preparing data for training...")

# Features and target
X = df.drop('risk_level', axis=1)
y = df['risk_level']

print(f"✅ Features: {list(X.columns)}")
print(f"✅ Target: risk_level (0-3)")

# Train-test split (80-20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42, 
    stratify=y  # Keep same distribution in train/test
)

print(f"✅ Training samples: {len(X_train)}")
print(f"✅ Testing samples: {len(X_test)}")

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"✅ Features scaled (StandardScaler)")

# ============================================================================
# STEP 3: TRAIN RANDOM FOREST MODEL
# ============================================================================

print("\n[STEP 3] Training Random Forest model...")

model = RandomForestClassifier(
    n_estimators=100,      # 100 trees (good balance of speed/accuracy)
    max_depth=15,          # Prevent overfitting
    min_samples_split=5,   # Min samples to split a node
    random_state=42,       # Reproducible results
    n_jobs=-1              # Use all CPU cores
)

# Train
model.fit(X_train_scaled, y_train)

print(f"✅ Model trained with {model.n_estimators} trees")

# ============================================================================
# STEP 4: EVALUATE MODEL
# ============================================================================

print("\n[STEP 4] Evaluating model performance...")

# Predictions
y_train_pred = model.predict(X_train_scaled)
y_test_pred = model.predict(X_test_scaled)

# Accuracy
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

print(f"\n{'='*70}")
print(f"  MODEL PERFORMANCE")
print(f"{'='*70}")
print(f"Training Accuracy:   {train_accuracy*100:.2f}%")
print(f"Testing Accuracy:    {test_accuracy*100:.2f}%")
print(f"Overfitting Gap:     {(train_accuracy - test_accuracy)*100:.2f}%")

if test_accuracy >= 0.90:
    print(f"\n✅ EXCELLENT! Model achieves {test_accuracy*100:.1f}% accuracy")
elif test_accuracy >= 0.85:
    print(f"\n✅ GOOD! Model achieves {test_accuracy*100:.1f}% accuracy")
else:
    print(f"\n⚠️  Model accuracy is {test_accuracy*100:.1f}% - consider tuning")

# Classification report
print(f"\nDetailed Classification Report:")
print("="*70)
print(classification_report(
    y_test, 
    y_test_pred, 
    target_names=['Safe', 'Warning', 'High Risk', 'Critical']
))

# Feature importance
print(f"\nFeature Importance (Top 5):")
print("="*70)
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

for idx, row in feature_importance.head(5).iterrows():
    print(f"{row['feature']:20s} {row['importance']:.4f}")

# ============================================================================
# STEP 5: SAVE MODEL AND SCALER
# ============================================================================

print(f"\n[STEP 5] Saving model for deployment...")

# Create models directory
os.makedirs('models', exist_ok=True)

# Save model
model_path = 'models/flood_model.pkl'
joblib.dump(model, model_path)
print(f"✅ Model saved: {model_path}")

# Save scaler
scaler_path = 'models/scaler.pkl'
joblib.dump(scaler, scaler_path)
print(f"✅ Scaler saved: {scaler_path}")

# Save feature names (for later use)
feature_names_path = 'models/feature_names.txt'
with open(feature_names_path, 'w') as f:
    f.write('\n'.join(X.columns))
print(f"✅ Feature names saved: {feature_names_path}")

# ============================================================================
# STEP 6: TEST PREDICTION FUNCTION
# ============================================================================

print(f"\n[STEP 6] Testing prediction function...")

# Test with example scenarios
test_scenarios = [
    {
        'name': 'Safe Conditions',
        'features': {
            'rainfall': 20, 'humidity': 60, 'river_level': 4,
            'temperature': 28, 'wind_speed': 10, 'month': 3,
            'soil_moisture': 40, 'elevation': 200, 'drainage_density': 8,
            'land_use_index': 3
        }
    },
    {
        'name': 'Warning Level',
        'features': {
            'rainfall': 80, 'humidity': 75, 'river_level': 7,
            'temperature': 26, 'wind_speed': 20, 'month': 7,
            'soil_moisture': 70, 'elevation': 100, 'drainage_density': 5,
            'land_use_index': 6
        }
    },
    {
        'name': 'High Risk',
        'features': {
            'rainfall': 150, 'humidity': 85, 'river_level': 10,
            'temperature': 25, 'wind_speed': 35, 'month': 8,
            'soil_moisture': 85, 'elevation': 40, 'drainage_density': 3,
            'land_use_index': 8
        }
    },
    {
        'name': 'Critical Alert',
        'features': {
            'rainfall': 250, 'humidity': 95, 'river_level': 14,
            'temperature': 24, 'wind_speed': 45, 'month': 9,
            'soil_moisture': 95, 'elevation': 10, 'drainage_density': 1,
            'land_use_index': 10
        }
    }
]

risk_labels = ['Safe', 'Warning', 'High Risk', 'Critical']

print("\nTest Predictions:")
print("="*70)

for scenario in test_scenarios:
    # Explicitly type cast for linter to understand
    scenario_dict = scenario  # type: ignore
    features_dict = scenario_dict['features']
    
    # Create feature array and ensure correct column order
    features_df = pd.DataFrame([features_dict])
    features_df = features_df[X.columns]  # Match exact order from training data
    features_scaled = scaler.transform(features_df)
    
    # Predict
    prediction = model.predict(features_scaled)[0]
    probability = model.predict_proba(features_scaled)[0]
    
    print(f"\n{scenario_dict['name']}:")
    print(f"  Input: Rainfall={features_dict['rainfall']}mm, " # type: ignore
          f"River={features_dict['river_level']}m") # type: ignore
    print(f"  Prediction: {risk_labels[prediction]}")
    print(f"  Confidence: {probability[prediction]*100:.1f}%")

# ============================================================================
# DONE!
# ============================================================================

print(f"\n{'='*70}")
print(f"  ✅ MODEL TRAINING COMPLETE!")
print(f"{'='*70}")
print(f"\nFiles created:")
print(f"  📄 data/flood_data.csv         - Training dataset")
print(f"  🤖 models/flood_model.pkl      - Trained model")
print(f"  📊 models/scaler.pkl           - Feature scaler")
print(f"  📝 models/feature_names.txt    - Feature list")
print(f"\nModel Stats:")
print(f"  🎯 Accuracy: {test_accuracy*100:.1f}%")
print(f"  📊 Samples: {len(df)}")
print(f"  🌲 Trees: {model.n_estimators}")
print(f"\nNext Step: Run 'streamlit run app.py' to build the dashboard!")
print(f"{'='*70}\n")