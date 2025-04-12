import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
from model.super_res_model import predict_aqi_map
import base64
import os
from fpdf import FPDF
from io import BytesIO
from city_coordinates import city_coords
import plotly.graph_objects as go
import pyttsx3

#Twilio Setup for WhatsApp Alerts
from twilio.rest import Client

# Twilio credentials (replace with your real credentials or use environment variables)
account_sid = "your_api_key"
auth_token = "your_auth_token"
twilio_client = Client(account_sid, auth_token)

def send_aqi_alert(user_number, location, aqi_value):
    message = twilio_client.messages.create(
        from_='whatsapp:+14155238886',  # Twilio sandbox WhatsApp number
        to=f'whatsapp:{user_number}',
        body=f'🌫 AQI Alert for {location}!\nCurrent AQI: {aqi_value}\n'
    )
    print("WhatsApp alert sent. SID:", message.sid)

def check_and_notify_aqi(aqi_value, user_number, location):
    if aqi_value > 150:  # Threshold
        send_aqi_alert(user_number, location, aqi_value)

#AQI Category Based on AQI Value
def get_aqi_category(aqi):
    if aqi <= 50:
        return "🟢 Good"
    elif aqi <= 100:
        return "🟡 Satisfactory"
    elif aqi <= 200:
        return "🟠 Moderate"
    elif aqi <= 300:
        return "🔴 Poor"
    elif aqi <= 400:
        return "🟣 Very Poor"
    else:
        return "⚫ Critical"


#Voice Alerts
def speak_aqi_alert(aqi, label):
    engine = pyttsx3.init()
    message = f"The Air Quality Index is {aqi}, categorized as {label}."
    engine.say(message)
    engine.runAndWait()


#AQI Meter
def show_aqi_meter(aqi_value):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=aqi_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Air Quality Index", 'font': {'size': 24}},
        delta={'reference': 100, 'increasing': {'color': "red"}},
        gauge={
            'axis': {'range': [0, 500], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "#009966"},
                {'range': [51, 100], 'color': "#ffde33"},
                {'range': [101, 200], 'color': "#ff9933"},
                {'range': [201, 300], 'color': "#cc0033"},
                {'range': [301, 400], 'color': "#660099"},
                {'range': [401, 500], 'color': "#7e0023"},
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': aqi_value
            }
        }
    ))

    fig.update_layout(paper_bgcolor="lavender", font={'color': "darkblue", 'family': "Arial"})
    st.plotly_chart(fig)


#Setting up UI
st.set_page_config(page_title="AQI Downscaler", layout="wide")
st.title("🌐 AI-Powered AQI Downscaler")
st.markdown("Convert low-res satellite data into high-res street-level AQI estimates. 📡")

#Sidebar
with st.sidebar:

    st.header("📍 Location")
    city_names = list(city_coords.keys())
    selected_city = st.selectbox("Select a City", [""] + city_names)

    default_lat = 28.6139
    default_lon = 77.2090

    if selected_city:
        default_lat, default_lon = city_coords[selected_city]

    lat = st.number_input("Latitude", value=default_lat, format="%.6f")
    lon = st.number_input("Longitude", value=default_lon, format="%.6f")

    date = st.date_input("Date", value=datetime.now().date())

    user_phone = st.text_input("📱 Enter your WhatsApp number", value="+91")

    # AQI Prediction
    if st.button("🔍 Get AQI"):
        st.session_state['aqi'] = predict_aqi_map(lat, lon)
        st.session_state['voice_alert_triggered'] = False
        st.session_state['alert_sent'] = False

    if 'aqi' in st.session_state:
        aqi_value = st.session_state['aqi']
        st.success(f"Predicted AQI: {aqi_value}")

        show_aqi_meter(aqi_value)
        category = get_aqi_category(aqi_value)
        st.markdown(f"### 🧾 Air Quality Category: **{category}**")

        if 'voice_alert_triggered' not in st.session_state or not st.session_state['voice_alert_triggered']:
            speak_aqi_alert(aqi_value, category)
            st.session_state['voice_alert_triggered'] = True
            # Send WhatsApp alert (once per session because of limited access in free plan)
            if not st.session_state.get('alert_sent', False):
                check_and_notify_aqi(aqi_value, user_phone, selected_city or "Unknown Location")
                st.session_state['alert_sent'] = True

st.subheader("🗺 AQI Map")
map_obj = folium.Map(location=[lat, lon], zoom_start=12)

if 'aqi' in st.session_state:
    folium.CircleMarker(
        location=[lat, lon],
        radius=15,
        popup=f"AQI: {st.session_state['aqi']}",
        color="red" if st.session_state['aqi'] > 100 else "green",
        fill=True,
        fill_opacity=0.6
    ).add_to(map_obj)
    st.success(f"Predicted AQI: {st.session_state['aqi']}")

st_data = st_folium(map_obj, width=700)

#Model Output
st.subheader("🧠 AI Model Output (Image)")
if st.button("🖼️ Show Model Output"):
    img_path = predict_aqi_map(lat, lon, output_image=True)
    st.image(img_path, caption="Super-Resolution Output", use_container_width=True)

#Report Download in CSV/PDF
st.subheader("📄 Download AQI Report")

report = pd.DataFrame({
    "Latitude": [lat],
    "Longitude": [lon],
    "Date": [date],
    "AQI": [st.session_state.get('aqi', 'N/A')]
})

if st.button("📥 Download CSV"):
    csv = report.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="aqi_report.csv">📥 Click here to download your AQI report</a>'
    st.markdown(href, unsafe_allow_html=True)

if st.button("📝 Download PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Air Quality Report", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Date: {date}", ln=True)
    pdf.cell(200, 10, txt=f"Latitude: {lat}", ln=True)
    pdf.cell(200, 10, txt=f"Longitude: {lon}", ln=True)
    pdf.cell(200, 10, txt=f"Predicted AQI: {st.session_state.get('aqi', 'N/A')}", ln=True)

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    b64_pdf = base64.b64encode(pdf_bytes).decode()

    pdf_href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="aqi_report.pdf">📝 Click here to download your PDF report</a>'
    st.markdown(pdf_href, unsafe_allow_html=True)
