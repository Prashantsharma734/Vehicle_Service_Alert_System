import streamlit as st
from datetime import datetime, timedelta
import pickle
from sms_service import send_sms

# Load ML model
model = pickle.load(open("model.pkl", "rb"))

st.set_page_config(page_title="Vehicle Service Alert", page_icon="🚗")

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN ----------------
if not st.session_state.logged_in:

    st.title("🔐 Login")

    name = st.text_input("Enter Your Name")

    col1, col2 = st.columns([1, 3])

    with col1:
        country_code = st.text_input("Code", value="+91", disabled=True)

    with col2:
        number = st.text_input("Phone Number")

    if st.button("Login"):

        if name and number and len(number) == 10 and number.isdigit():

            st.session_state.logged_in = True
            st.session_state.name = name
            st.session_state.phone = country_code + number

            st.rerun()

        else:
            st.error("Enter valid details")

# ---------------- MAIN APP ----------------
else:

    st.title("🚗 Smart AI Vehicle Service Alert System")
    st.write(f"Welcome, {st.session_state.name} 👋")

    st.header("📅 Service Date Details")

    last_service_date = st.date_input("Last Service Date")
    service_interval_days = st.number_input("Service Interval (Days)", value=90)

    st.header("🚘 Vehicle Details (AI Prediction)")

    mileage = st.number_input("Mileage")
    vehicle_age = st.number_input("Vehicle Age (years)")
    engine_size = st.number_input("Engine Size")
    odometer = st.number_input("Odometer Reading")
    fuel_eff = st.number_input("Fuel Efficiency")

    if st.button("🔍 Check Service Status"):

        # ---------------- DATE LOGIC ----------------
        next_service_date = last_service_date + timedelta(days=service_interval_days)
        today = datetime.today().date()

        st.subheader("📅 Next Service Date")
        st.write(next_service_date)

        # ---------------- ML PREDICTION ----------------
        prediction = model.predict([[mileage, vehicle_age, engine_size, odometer, fuel_eff]])

        st.subheader("🤖 AI Prediction")
        if prediction[0] >= 0.5:
            st.warning("⚠️ AI says maintenance required")
            ai_flag = True
        else:
            st.success("✅ AI says vehicle is fine")
            ai_flag = False

        # ---------------- FINAL ALERT ----------------
        if today >= next_service_date or ai_flag:

            alert = f"{st.session_state.name}, your vehicle needs servicing!"

            st.error(alert)

            success = send_sms(alert, st.session_state.phone)

            if success:
                st.success("📩 SMS Sent")
            else:
                st.warning("❌ SMS Failed")

        elif (next_service_date - today).days <= 7:
            st.warning("⚠️ Service Due Soon")

        else:
            st.success("✅ No Service Needed")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()