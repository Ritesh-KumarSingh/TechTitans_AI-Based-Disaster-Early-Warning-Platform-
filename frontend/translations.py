"""
Translations - English and Hindi
All UI text for the Disaster Detection AI app
"""

TRANSLATIONS = {
    'en': {
        'app_name': '🛡️ Disaster Detection AI',
        'subtitle': 'Real-time Flood Risk Prediction • Powered by Machine Learning',
        'search_heading': '📍 Check Disaster Risk for Your City',
        'search_placeholder': 'Enter city name (e.g., Mumbai, Delhi, Chennai...)',
        'search_btn': '🔍 Analyze Risk',
        'select_disaster': 'Select Disaster',
        'disaster_flood': '🌊 Flood',
        'disaster_cyclone': '🌀 Cyclone',
        'disaster_heatwave': '🌡️ Heatwave',
        'analyzing': '🌊 Analyzing risk with AI...',
        'error_title': 'Could not fetch weather data',
        'error_msg': 'Please check the city name and try again',
        'ai_confidence': 'AI Confidence',
        'risk_level': 'Risk Level',
        'temperature': 'Temperature',
        'humidity': 'Humidity',
        'wind_speed': 'Wind Speed',
        'risk_distribution': 'Risk Distribution',
        'recommended_actions': '🎯 Recommended Actions',
        'emergency_helpline': '🆘 EMERGENCY HELPLINE: 112 &nbsp;|&nbsp; 🚑 Ambulance: 108 &nbsp;|&nbsp; 👮 Police: 100 &nbsp;|&nbsp; 🚒 Fire: 101',
        'local_resources': '🏥 Local Emergency Resources',
        'hospitals': 'Hospitals',
        'shelters': 'Shelters',
        'current_weather': '🌤️ Current Weather in',
        'rainfall_1h': 'Rainfall (1h)',
        'pressure': 'Pressure',
        'ai_details': '🤖  AI Model Details',
        'features_used': 'Input features used for prediction:',
        'model_info': 'Random Forest (100 trees) • 89% Accuracy • 10 Features • 2,000 Training Samples • 4 Risk Levels',
        'footer_1': 'Built with ❤️ by TechTitans',
        'footer_2': 'Disaster Detection AI © 2026 • Saving Lives Through Technology',
        'api_missing_title': 'API Key Missing',
        'api_missing_msg': 'Please add your OpenWeatherMap API key to the',
        'risk_labels': {
            0: {'label': 'Safe', 'title': 'All Clear', 'message': 'No immediate threat detected. Conditions are normal.'},
            1: {'label': 'Warning', 'title': 'Stay Alert', 'message': 'Elevated risk conditions detected. Monitor closely.'},
            2: {'label': 'High Risk', 'title': 'Take Action Now', 'message': 'Significant risk likely. Take precautions immediately!'},
            3: {'label': 'Critical', 'title': 'SEVERE ALERT', 'message': 'SEVERE HAZARD IMMINENT! Take extreme precautions or evacuate!'}
        },
        'risk_actions': {
            0: ['📰 Stay updated with weather news', '📋 Review emergency preparedness plan', '🎒 Keep emergency kit accessible', '😊 Enjoy your day safely'],
            1: ['🧰 Prepare emergency supplies', '🔋 Charge all devices', '🏔️ Avoid risky areas', '📱 Monitor local weather updates', '📄 Secure important documents'],
            2: ['📦 Secure valuables', '🚪 Prepare contingency plan', '⚡ Be ready for power outages', '🏔️ Stay in safe structures', '🚫 Avoid unnecessary travel', '🧰 Keep emergency supplies ready'],
            3: ['🆘 SEEK IMMEDIATE SAFETY', '📞 Call emergency services: 112', '🚫 Do NOT venture outside', '🏢 Stay in fortified structures', '🏳️ Signal for help if stranded', '🗺️ Follow official instructions']
        },
        'prob_labels': ['Safe', 'Warning', 'High Risk', 'Critical']
    },
    'hi': {
        'app_name': '🛡️ आपदा पहचान AI',
        'subtitle': 'रियल-टाइम बाढ़ जोखिम भविष्यवाणी • मशीन लर्निंग द्वारा संचालित',
        'search_heading': '📍 अपने शहर के लिए आपदा जोखिम जांचें',
        'search_placeholder': 'शहर का नाम दर्ज करें (जैसे, मुंबई, दिल्ली, चेन्नई...)',
        'search_btn': '🔍 जोखिम जांचें',
        'select_disaster': 'आपदा चुनें (Select Disaster)',
        'disaster_flood': '🌊 बाढ़ (Flood)',
        'disaster_cyclone': '🌀 चक्रवात (Cyclone)',
        'disaster_heatwave': '🌡️ लू (Heatwave)',
        'analyzing': '🌊 AI से जोखिम का विश्लेषण हो रहा है...',
        'error_title': 'मौसम डेटा प्राप्त नहीं हो सका',
        'error_msg': 'कृपया शहर का नाम जांचें और पुनः प्रयास करें',
        'ai_confidence': 'AI विश्वसनीयता',
        'risk_level': 'जोखिम स्तर',
        'temperature': 'तापमान',
        'humidity': 'आर्द्रता',
        'wind_speed': 'हवा की गति',
        'risk_distribution': 'जोखिम वितरण',
        'recommended_actions': '🎯 अनुशंसित कार्रवाई',
        'emergency_helpline': '🆘 आपातकालीन हेल्पलाइन: 112 &nbsp;|&nbsp; 🚑 एम्बुलेंस: 108 &nbsp;|&nbsp; 👮 पुलिस: 100 &nbsp;|&nbsp; 🚒 दमकल: 101',
        'local_resources': '🏥 स्थानीय आपातकालीन संसाधन',
        'hospitals': 'अस्पताल',
        'shelters': 'आश्रय स्थल',
        'current_weather': '🌤️ वर्तमान मौसम -',
        'rainfall_1h': 'वर्षा (1 घंटा)',
        'pressure': 'दबाव',
        'ai_details': '🤖  AI मॉडल विवरण',
        'features_used': 'भविष्यवाणी के लिए उपयोग किए गए इनपुट फीचर्स:',
        'model_info': 'रैंडम फॉरेस्ट (100 ट्री) • 89% सटीकता • 10 फीचर्स • 2,000 ट्रेनिंग सैंपल • 4 जोखिम स्तर',
        'footer_1': 'Built with ❤️ by TechTitans',
        'footer_2': 'Disaster Detection AI © 2026 • Saving Lives Through Technology',
        'api_missing_title': 'API कुंजी गुम है',
        'api_missing_msg': 'कृपया अपनी OpenWeatherMap API कुंजी .env फ़ाइल में जोड़ें',
        'risk_labels': {
            0: {'label': 'सुरक्षित', 'title': 'सब ठीक है', 'message': 'कोई खतरा नहीं। स्थितियाँ सामान्य हैं।'},
            1: {'label': 'चेतावनी', 'title': 'सतर्क रहें', 'message': 'जोखिम का पता चला। स्थिति पर नज़र रखें।'},
            2: {'label': 'उच्च जोखिम', 'title': 'अभी कार्रवाई करें', 'message': 'भारी जोखिम की संभावना। तुरंत सावधानी बरतें!'},
            3: {'label': 'गंभीर', 'title': 'गंभीर अलर्ट', 'message': 'गंभीर खतरा आसन्न! अत्यंत सावधानी बरतें या सुरक्षित स्थान पर जाएँ!'}
        },
        'risk_actions': {
            0: ['📰 मौसम समाचार से अपडेट रहें', '📋 आपातकालीन तैयारी योजना की समीक्षा करें', '🎒 आपातकालीन किट तैयार रखें', '😊 सुरक्षित रूप से अपने दिन का आनंद लें'],
            1: ['🧰 आपातकालीन आपूर्ति तैयार करें', '🔋 सभी उपकरण चार्ज करें', '🏔️ जोखिम वाले इलाकों से बचें', '📱 स्थानीय मौसम अपडेट देखें', '📄 महत्वपूर्ण दस्तावेज़ सुरक्षित करें'],
            2: ['📦 कीमती सामान सुरक्षित करें', '🚪 आकस्मिक योजना तैयार रखें', '⚡ बिजली कटौती के लिए तैयार रहें', '🏔️ सुरक्षित संरचनाओं में रहें', '🚫 अनावश्यक यात्रा से बचें', '🧰 आपातकालीन आपूर्ति तैयार रखें'],
            3: ['🆘 तत्काल सुरक्षा प्राप्त करें', '📞 आपातकालीन सेवाएं कॉल करें: 112', '🚫 बाहर न निकलें', '🏢 मजबूत संरचनाओं में रहें', '🏳️ फंसे हों तो मदद के लिए संकेत दें', '🗺️ आधिकारिक निर्देशों का पालन करें']
        },
        'prob_labels': ['सुरक्षित', 'चेतावनी', 'उच्च जोखिम', 'गंभीर']
    }
}


def t(key, lang='en'):
    """Get translation for a key"""
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, TRANSLATIONS['en'].get(key, key))
