import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get API Key
API_KEY = os.getenv("API_KEY")

# 🎯 Streamlit App Title
st.title("💰 Real-time Currency Converter")

# Supported Currencies (For UI Dropdowns)
supported_currencies = ["USD", "EUR", "GBP", "INR", "PKR", "CAD", "AUD"]

# User Inputs
from_currency = st.selectbox("From Currency", supported_currencies)
to_currency = st.selectbox("To Currency", supported_currencies)
amount = st.number_input("Enter Amount:", min_value=1.0, step=1.0)

# Convert Currency
if st.button("Convert"):
    if not API_KEY:
        st.error("⚠️ API Key is missing! Please check your .env file.")
    else:
        try:
            # Construct API URL using API_KEY
            url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_currency}/{to_currency}/{amount}"

            # Fetch Data from API
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                converted_amount = data.get("conversion_result")
                rate = data.get("conversion_rate")

                if converted_amount is not None and rate is not None:
                    # Display Result
                    st.success(f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")
                    st.info(f"Exchange Rate: 1 {from_currency} = {rate:.4f} {to_currency}")
                else:
                    st.error("⚠️ Unexpected API Response Format")
            else:
                st.error(f"⚠️ API Error! Response Code: {response.status_code}")
        except Exception as e:
            st.error(f"⚠️ Something went wrong: {e}")
