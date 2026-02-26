"""
Frontend Styles - Modern Glassmorphism CSS
All CSS for the Disaster Detection AI dashboard
"""

import streamlit as st


def apply_styles():
    """Inject all glassmorphism CSS into the Streamlit app"""
    st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * { font-family: 'Poppins', sans-serif !important; box-sizing: border-box; }
    
    /* Hide Streamlit defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Dark gradient background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    /* Glass card */
    .glass-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Hero section */
    .hero {
        text-align: center;
        padding: 2rem 0 1.5rem 0;
        overflow: visible;
    }
    
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1.4;
        letter-spacing: -0.5px;
        display: block;
    }
    
    .hero-subtitle {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1.05rem;
        font-weight: 300;
        margin-top: 0.8rem;
        line-height: 1.5;
    }
    
    /* Risk result card */
    .risk-result {
        border-radius: 24px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .risk-result::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .risk-result h1 {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        position: relative;
        line-height: 1.4;
    }
    
    .risk-result h2 {
        font-size: 1.3rem;
        font-weight: 400;
        margin: 0.8rem 0;
        opacity: 0.95;
        position: relative;
        line-height: 1.4;
    }
    
    .risk-result p {
        font-size: 1rem;
        position: relative;
        line-height: 1.6;
        margin: 0.5rem 0;
    }
    
    /* Metric glass cards */
    .metric-glass {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 1.2rem 1rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 0.2rem;
        overflow: hidden;
    }
    
    .metric-glass:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
    }
    
    .metric-icon { font-size: 1.6rem; line-height: 1; margin: 0; }
    
    .metric-value {
        font-size: 1.4rem;
        font-weight: 700;
        color: white;
        margin: 0;
        line-height: 1.3;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 100%;
    }
    
    .metric-label {
        font-size: 0.65rem;
        color: rgba(255, 255, 255, 0.5);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 500;
        line-height: 1.2;
        margin: 0;
    }
    
    /* Action chips */
    .action-chip {
        display: inline-block;
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        padding: 0.6rem 1.2rem;
        border-radius: 50px;
        margin: 0.3rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.85rem;
        font-weight: 400;
        line-height: 1.4;
        transition: all 0.3s ease;
        vertical-align: middle;
    }
    
    .action-chip:hover {
        background: rgba(255, 255, 255, 0.15);
        transform: scale(1.03);
    }
    
    /* Emergency banner */
    .emergency-banner {
        background: linear-gradient(135deg, #f5576c, #ff6b6b);
        color: white;
        padding: 1.2rem 2rem;
        border-radius: 16px;
        font-size: 1.1rem;
        font-weight: 600;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 8px 30px rgba(245, 87, 108, 0.4);
        animation: pulse 2s infinite;
    }
    
    /* Weather widget */
    .weather-glass {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
    }
    
    .weather-glass h3 {
        color: rgba(255, 255, 255, 0.9);
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .weather-detail {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.7rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        line-height: 1.4;
    }
    
    .weather-detail-label {
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.85rem;
        line-height: 1.4;
    }
    
    .weather-detail-value {
        color: white;
        font-weight: 600;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    
    /* Animations */
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    
    .fade-in { animation: fadeInUp 0.6s ease-out forwards; }
    .fade-in-delay { animation: fadeInUp 0.6s ease-out 0.2s forwards; opacity: 0; }
    .fade-in-delay-2 { animation: fadeInUp 0.6s ease-out 0.4s forwards; opacity: 0; }
    
    /* Input styling */
    .stTextInput input {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 16px !important;
        padding: 0.9rem 1.2rem !important;
        font-size: 1rem !important;
        color: white !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stTextInput input::placeholder { color: rgba(255, 255, 255, 0.4) !important; }
    .stTextInput input:focus { border-color: rgba(102, 126, 234, 0.6) !important; box-shadow: 0 0 20px rgba(102, 126, 234, 0.2) !important; }
    .stTextInput label { color: rgba(255, 255, 255, 0.7) !important; font-weight: 500 !important; }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 0.8rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.35) !important;
        transition: all 0.3s ease !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.5) !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        color: rgba(255, 255, 255, 0.8) !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.95) !important;
        backdrop-filter: blur(20px) !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown { color: rgba(255, 255, 255, 0.8) !important; }
    
    /* Divider */
    hr { border-color: rgba(255, 255, 255, 0.08) !important; }
    
    /* Info/Warning boxes */
    .stAlert { background: rgba(255, 255, 255, 0.05) !important; border-radius: 12px !important; }
    
    /* Dataframe */
    .stDataFrame { border-radius: 12px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)
