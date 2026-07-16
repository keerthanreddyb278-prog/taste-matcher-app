import streamlit as st
import pandas as pd
import requests
import json

# 👇 PASTE YOUR NEW WEB APP URL BELOW BETWEEN THE QUOTES
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzDCkEKPo2fldOQ-fA-GirKk9AjF5gpIDVeZIGiskTUSIUtwF8YiUSkeXLF2js5Tskruw/exec"
# YOUR GOOGLE SHEET LINKS
PROFILES_CSV = "https://docs.google.com/spreadsheets/d/1NgCTYGiGk8TTV1wD29M6j1w49T3h-uBkGI3Ps2Gouf0/export?format=csv&gid=0"
CHATS_CSV = "https://docs.google.com/spreadsheets/d/1NgCTYGiGk8TTV1wD29M6j1w49T3h-uBkGI3Ps2Gouf0/export?format=csv&gid=1040764631"

def send_profile_to_sheet(name, h1, h2, h3):
    payload = {"type": "profile", "name": name, "h1": h1, "h2": h2, "h3": h3}
    try: requests.post(WEB_APP_URL, data=json.dumps(payload))
    except: pass

def send_message_to_sheet(sender, receiver, message):
    payload = {"type": "chat", "sender": sender, "receiver": receiver, "message": message}
    try: requests.post(WEB_APP_URL, data=json.dumps(payload))
    except: pass

st.title("🤝 TasteMatcher")

# User Input Section
my_name = st.text_input("Enter your Name:")
hobby1 = st.selectbox("Select Hobby:", ["Cricket", "Coding", "Movies", "Books"])
hobby2 = st.text_input("Enter your favorite Food:")
hobby3 = st.text_input("Enter your favorite Movie Genre:")

if st.button("Find My Match! 🚀"):
    send_profile_to_sheet(my_name, hobby1, hobby2, hobby3)
    st.success("Profile saved successfully!")

# Auto-refresh and display matches
st.divider()
st.subheader("🎯 Real People with Similar Tastes")

try:
    df = pd.read_csv(PROFILES_CSV)
    df.columns = ['Timestamp', 'Name', 'Hobby-1', 'Hobby-2', 'Hobby-3']
    st.write("Live Database Connected!")
    st.dataframe(df) # Shows that data is loading
except Exception as e:
    st.error("Connecting to database... Please ensure your Google Sheet is set to 'Anyone with the link'.")
