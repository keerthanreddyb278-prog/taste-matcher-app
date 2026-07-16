import streamlit as st
import requests
import json

# Replace this with your actual Google Apps Script Web App URL
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxh_PjiLJ88nTMDCXVtKeIHJbE2stQrNQWIIL_WvDtSDpdw2yjCxAgmrcda8Ewn42Sqxg/exec"

st.title("TasteMatcher Pro")

# Form to submit data
with st.form("profile_form"):
    st.subheader("Create Your Profile")
    name = st.text_input("Name")
    hobby = st.text_input("Hobby")
    food = st.text_input("Favorite Food")
    game = st.text_input("Favorite Game")
    
    # Save button
    submit_button = st.form_submit_button("Save Profile")
    
    if submit_button:
        payload = {
            "name": name,
            "hobby": hobby,
            "food": food,
            "game": game
        }
        try:
            # Sending data to Google Sheets
            response = requests.post(WEB_APP_URL, data=json.dumps(payload))
            if response.status_code == 200:
                st.success("Profile saved successfully!")
            else:
                st.error("Failed to save. Check your URL.")
        except Exception as e:
            st.error(f"Error: {e}")
