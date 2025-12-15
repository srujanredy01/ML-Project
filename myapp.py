import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load trained model
model = joblib.load("gbr_model.pkl")

st.set_page_config(page_title="Bike Demand Prediction", layout="wide")

st.title("🚲 Bike Demand Prediction Dashboard")
st.write("Enter feature values to predict bike demand")

# --- Input Section ---
col1, col2, col3 = st.columns(3)

with col1:
    season = st.selectbox("Season (1-4)", [1, 2, 3, 4])
    weather = st.selectbox("Weather (1-4)", [1, 2, 3, 4])
    hour = st.slider("Hour", 0, 23)
    weekday = st.slider("Weekday (0=Sun)", 0, 6)
    is_weekend = st.selectbox("Is Weekend", [0, 1])

with col2:
    temp = st.slider("Temperature", 0.0, 1.0)
    humidity = st.slider("Humidity", 0.0, 1.0)
    windspeed = st.slider("Windspeed", 0.0, 1.0)
    casual = st.number_input("Casual Riders", min_value=0)
    registered = st.number_input("Registered Riders", min_value=0)

with col3:
    day = st.slider("Day", 1, 31)
    month = st.slider("Month", 1, 12)
    year = st.selectbox("Year", [2011, 2012])
    total_riders = casual + registered

# --- Feature Engineering ---
temp_humidity = temp * humidity
temp_windspeed = temp * windspeed

hour_sin = np.sin(2 * np.pi * hour / 24)
hour_cos = np.cos(2 * np.pi * hour / 24)

month_sin = np.sin(2 * np.pi * month / 12)
month_cos = np.cos(2 * np.pi * month / 12)

weekday_sin = np.sin(2 * np.pi * weekday / 7)
weekday_cos = np.cos(2 * np.pi * weekday / 7)

# --- Create Input DataFrame ---
input_data = pd.DataFrame([{
    "season": season,
    "weather": weather,
    "temp": temp,
    "humidity": humidity,
    "windspeed": windspeed,
    "casual": casual,
    "registered": registered,
    "hour": hour,
    "day": day,
    "month": month,
    "year": year,
    "weekday": weekday,
    "is_weekend": is_weekend,
    "temp_humidity": temp_humidity,
    "temp_windspeed": temp_windspeed,
    "total_riders": total_riders,
    "hour_sin": hour_sin,
    "hour_cos": hour_cos,
    "month_sin": month_sin,
    "month_cos": month_cos,
    "weekday_sin": weekday_sin,
    "weekday_cos": weekday_cos
}])

# --- Prediction ---
if st.button("Predict Demand"):
    prediction = model.predict(input_data)[0]
    st.success(f"### Predicted Bike Demand: {int(prediction)} 🚴‍♂️")

    st.subheader("Input Summary")
    st.dataframe(input_data)
