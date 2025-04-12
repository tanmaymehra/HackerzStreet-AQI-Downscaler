
# 🌐 AI-Powered AQI Downscaler

A Streamlit-based application that leverages AI to transform coarse satellite air quality data into high-resolution, street-level AQI (Air Quality Index) insights. The platform features an interactive map, real-time voice alerts, WhatsApp notifications, predictive analytics, and downloadable AQI reports in PDF/CSV formats.

---

## 🚀 Features

- 📍 **Location-Based AQI Prediction**  
  Predict air quality by selecting a city or entering custom coordinates.

- 🧠 **AI Downscaling Model**  
  Simulated super-resolution model to emulate downscaling of satellite imagery (with placeholder image for demonstration).

- 🗺️ **Interactive AQI Map**  
  Visual representation of AQI using color-coded map markers powered by Folium.

- 📊 **Gauge Meter**  
  Real-time AQI visualized using a dynamic gauge via Plotly.

- 🔊 **Voice Alerts**  
  Get verbal updates about the air quality through built-in text-to-speech.

- 💬 **WhatsApp Notifications**  
  Automatically receive alerts if AQI exceeds a health-risk threshold using Twilio.

- 📄 **Report Downloads**  
  Download AQI reports in both CSV and PDF formats with geo-tagged summaries.

---

## 📂 Project Structure

```plaintext
├── app.py                    # Main Streamlit application
├── model/
│   └── super_res_model.py    # Dummy model for AQI prediction and image path
├── city_coordinates.py       # Predefined city-to-coordinates mapping
├── requirements.txt          # Python dependencies
├── data/
│   └── satellite_sample.png  # Dummy image used for "model output"
```

---

## ⚙️ Installation & Setup

1. **Clone the repo**
```bash
git clone https://github.com/tanmaymehra/HackerzStreet-AQI-Downscaler/
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Add Twilio credentials**
Create a `.env` file (or replace placeholders in `app.py`) with:
```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
```

5. **Run the app**
```bash
streamlit run app.py
```

---

## 📦 Requirements

```txt
streamlit
pandas
folium
streamlit-folium
plotly
fpdf
Pillow
twilio
pyttsx3
```

---


## 📈 Future Enhancements

- Replace dummy model with a real trained super-resolution model (e.g. SRCNN, ESRGAN).
- Add spatiotemporal forecasting (e.g. LSTM) for short-term AQI predictions.
- Integrate Mapbox or Google Maps for higher-resolution layers.
- Mobile-friendly interface and push notifications.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
