"""
Disaster Detection AI
10-Hour Hackathon MVP
Modern glassmorphism UI with ML-powered flood risk prediction

Project Structure:
├── app.py              ← This file (main entry point)
├── frontend/           ← UI: styles, translations, charts
├── backend/            ← Logic: weather API, prediction, features
├── ml_model/           ← ML: trainer, saved models, training data
"""

import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

# Import from project modules
from frontend.styles import apply_styles
from frontend.translations import TRANSLATIONS, t
from frontend.charts import create_risk_gauge, create_prob_chart
from backend.weather_api import get_weather_data
from backend.predictor import (
    load_model as _load_model,
    transform_to_features,
    predict_flood_risk,
    EMERGENCY_RESOURCES,
)

# Load environment variables
load_dotenv()

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Disaster Detection AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply glassmorphism styles
apply_styles()

# ============================================================================
# MODEL LOADING (cached)
# ============================================================================

@st.cache_resource
def load_model():
    """Load trained ML model and scaler"""
    model_path = os.path.join(os.path.dirname(__file__), 'ml_model', 'saved_models')

    model_file = os.path.join(model_path, 'flood_model.pkl')
    scaler_file = os.path.join(model_path, 'scaler.pkl')

    if not os.path.exists(model_file) or not os.path.exists(scaler_file):
        st.error("❌ Model files not found! Run `python ml_model/trainer.py` first.")
        st.stop()

    import joblib
    model = joblib.load(model_file)
    scaler = joblib.load(scaler_file)
    return model, scaler


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application with modern glassmorphism UI"""

    # ── Language Toggle ──
    lang_col1, lang_col2, lang_col3 = st.columns([5, 2, 5])
    with lang_col2:
        lang_choice = st.toggle("हिंदी", value=False, help="Switch to Hindi / हिंदी में बदलें")
    lang = 'hi' if lang_choice else 'en'

    # ── Hero Section ──
    st.markdown(f"""
    <div class="hero fade-in">
        <div class="hero-title">{t('app_name', lang)}</div>
        <div class="hero-subtitle">{t('subtitle', lang)}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── API Key (silent load from .env) ──
    api_key = os.getenv('OPENWEATHER_API_KEY', '')

    if not api_key:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">⚠️</div>
            <h3 style="color: white; font-weight: 600; line-height: 1.4;">{t('api_missing_title', lang)}</h3>
            <p style="color: rgba(255,255,255,0.6); font-size: 0.95rem; line-height: 1.6;">
                {t('api_missing_msg', lang)}
                <code style="background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px;">.env</code>:<br>
                <code style="background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px;">OPENWEATHER_API_KEY=your_key_here</code>
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # Load model
    model, scaler = load_model()

    # ── Search Section ──
    st.markdown(f"""
    <div class="fade-in-delay" style="text-align: center; margin-bottom: 0.5rem;">
        <h3 style="color: rgba(255,255,255,0.8); font-weight: 500; line-height: 1.4;">
            {t('search_heading', lang)}
        </h3>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1])

    with col1:
        city = st.text_input(
            "City",
            placeholder=t('search_placeholder', lang),
            label_visibility="collapsed"
        )

    with col2:
        search_btn = st.button(t('search_btn', lang), use_container_width=True)

    # ── Prediction ──
    if search_btn and city:
        with st.spinner(t('analyzing', lang)):
            weather = get_weather_data(city, api_key)

            if not weather:
                st.markdown(f"""
                <div class="glass-card" style="text-align: center; border-color: rgba(239, 68, 68, 0.3);">
                    <div style="font-size: 3rem;">😕</div>
                    <h3 style="color: #ef4444;">{t('error_title', lang)}</h3>
                    <p style="color: rgba(255,255,255,0.5);">{t('error_msg', lang)}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                features = transform_to_features(weather)
                prediction = predict_flood_risk(features, model, scaler, TRANSLATIONS, lang)

                # ── Risk Result Card ──
                st.markdown(f"""
                <div class="risk-result fade-in" style="background: {prediction['gradient']};">
                    <h1>{prediction['emoji']} {prediction['title']}</h1>
                    <h2>📍 {weather['city']}</h2>
                    <p>{prediction['message']}</p>
                    <p style="opacity: 0.85; margin-top: 1rem;">
                        🤖 {t('ai_confidence', lang)}: <strong>{prediction['probability']*100:.0f}%</strong>
                    </p>
                </div>
                """, unsafe_allow_html=True)

                # ── Metric Cards ──
                st.markdown('<div class="fade-in-delay">', unsafe_allow_html=True)

                col1, col2, col3, col4 = st.columns(4)

                metrics_data = [
                    (col1, "🎯", prediction['label'], t('risk_level', lang), prediction['color']),
                    (col2, "🌡️", f"{weather['temperature']:.1f}°C", t('temperature', lang), "#667eea"),
                    (col3, "💧", f"{weather['humidity']}%", t('humidity', lang), "#764ba2"),
                    (col4, "💨", f"{weather['wind_speed']:.1f} km/h", t('wind_speed', lang), "#f093fb"),
                ]

                for col, icon, value, label, color in metrics_data:
                    with col:
                        st.markdown(f"""
                        <div class="metric-glass">
                            <div class="metric-icon">{icon}</div>
                            <div class="metric-label">{label}</div>
                            <div class="metric-value" style="color: {color};">{value}</div>
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

                # ── Gauge + Probability Charts ──
                st.markdown('<div class="fade-in-delay-2">', unsafe_allow_html=True)

                col_gauge, col_bars = st.columns(2)

                with col_gauge:
                    st.markdown('<div class="glass-card" style="padding: 1rem;">', unsafe_allow_html=True)
                    gauge_fig = create_risk_gauge(prediction['probability'], prediction['color'])
                    st.plotly_chart(gauge_fig, use_container_width=True, config={'displayModeBar': False})
                    st.markdown('</div>', unsafe_allow_html=True)

                with col_bars:
                    st.markdown(f"""
                    <div class="glass-card" style="padding: 1rem;">
                        <h4 style="color: rgba(255,255,255,0.7); text-align: center; margin-bottom: 0.5rem;">
                            {t('risk_distribution', lang)}
                        </h4>
                    """, unsafe_allow_html=True)
                    prob_fig = create_prob_chart(prediction['all_probs'])
                    st.plotly_chart(prob_fig, use_container_width=True, config={'displayModeBar': False})
                    st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

                # ── Action Chips ──
                st.markdown(f"""
                <div class="glass-card fade-in-delay-2">
                    <h3 style="color: rgba(255,255,255,0.9); margin-bottom: 1rem;">{t('recommended_actions', lang)}</h3>
                """, unsafe_allow_html=True)

                for action in prediction['actions']:
                    st.markdown(f'<div class="action-chip">{action}</div>', unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

                # ── Emergency Banner (if high risk) ──
                if prediction['risk_level'] >= 2:
                    st.markdown(f"""
                    <div class="emergency-banner">
                        {t('emergency_helpline', lang)}
                    </div>
                    """, unsafe_allow_html=True)

                    # City-specific resources
                    city_lower = city.lower()
                    for key, resources in EMERGENCY_RESOURCES.items():
                        if key in city_lower:
                            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                            st.markdown(f'<h3 style="color: rgba(255,255,255,0.9);">{t("local_resources", lang)}</h3>', unsafe_allow_html=True)

                            res_col1, res_col2 = st.columns(2)
                            with res_col1:
                                st.markdown(f'<p style="color: rgba(255,255,255,0.6); font-weight: 600;">{t("hospitals", lang)}</p>', unsafe_allow_html=True)
                                for h in resources['hospitals']:
                                    st.markdown(f'<div class="action-chip">{h}</div>', unsafe_allow_html=True)
                            with res_col2:
                                st.markdown(f'<p style="color: rgba(255,255,255,0.6); font-weight: 600;">{t("shelters", lang)}</p>', unsafe_allow_html=True)
                                for s in resources['shelters']:
                                    st.markdown(f'<div class="action-chip">{s}</div>', unsafe_allow_html=True)

                            st.markdown('</div>', unsafe_allow_html=True)
                            break

                # ── Weather Details ──
                st.markdown(f"""
                <div class="weather-glass fade-in-delay-2">
                    <h3>{t('current_weather', lang)} {weather['city']}</h3>
                    <div style="font-size: 3rem; text-align: center; margin: 1rem 0;">
                        {'🌧️' if weather['rainfall_1h'] > 0 else '☀️' if weather['temperature'] > 30 else '🌤️'}
                    </div>
                    <div style="text-align: center; font-size: 1.2rem; text-transform: capitalize; margin-bottom: 1.5rem;">
                        {weather['description']}
                    </div>
                    <div class="weather-detail">
                        <span class="weather-detail-label">🌡️ {t('temperature', lang)}</span>
                        <span class="weather-detail-value">{weather['temperature']:.1f}°C</span>
                    </div>
                    <div class="weather-detail">
                        <span class="weather-detail-label">💧 {t('humidity', lang)}</span>
                        <span class="weather-detail-value">{weather['humidity']}%</span>
                    </div>
                    <div class="weather-detail">
                        <span class="weather-detail-label">💨 {t('wind_speed', lang)}</span>
                        <span class="weather-detail-value">{weather['wind_speed']:.1f} km/h</span>
                    </div>
                    <div class="weather-detail">
                        <span class="weather-detail-label">🌧️ {t('rainfall_1h', lang)}</span>
                        <span class="weather-detail-value">{weather['rainfall_1h']:.1f} mm</span>
                    </div>
                    <div class="weather-detail" style="border: none;">
                        <span class="weather-detail-label">🌀 {t('pressure', lang)}</span>
                        <span class="weather-detail-value">{weather['pressure']} hPa</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # ── ML Features (expandable) ──
                with st.expander(t('ai_details', lang)):
                    st.markdown(f'<p style="color: rgba(255,255,255,0.7);">{t("features_used", lang)}</p>', unsafe_allow_html=True)

                    feature_df = pd.DataFrame([features]).T
                    feature_df.columns = ['Value']
                    feature_df.index.name = 'Feature'
                    st.dataframe(feature_df, use_container_width=True)

                    st.markdown(f"""
                    <div style="padding: 1rem; margin-top: 1rem; background: rgba(255,255,255,0.05); border-radius: 12px;">
                        <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin: 0;">
                            <strong style="color: rgba(255,255,255,0.8);">Model Info:</strong>
                            {t('model_info', lang)}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

    # ── Footer ──
    st.markdown(f"""
    <div style="text-align: center; padding: 3rem 0 1rem 0;">
        <div style="color: rgba(255,255,255,0.3); font-size: 0.85rem; line-height: 1.5;">
            {t('footer_1', lang)}
        </div>
        <div style="color: rgba(255,255,255,0.2); font-size: 0.75rem; margin-top: 0.3rem; line-height: 1.5;">
            {t('footer_2', lang)}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()