import streamlit as st
import pandas as pd
import requests, json

# Paste your Web App URL here inside the quotes
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyagcvfkDP2rJO1GyTIZyRrgId1kxQU8mIH7AgIyE2or5S2yoDj2sZH7uwfEyBJZw3ZXw/exec"
st.title("🤝 TasteMatcher Pro")

# 1. Profile Section
with st.form("profile_form"):
    name = st.text_input("Name")
    hobby = st.text_input("Hobby")
    food = st.text_input("Favorite Food")
    game = st.text_input("Favorite Game")
    submitted = st.form_submit_button("Save Profile")
    if submitted:
        payload = {"type": "profile", "name": name, "hobby": hobby, "food": food, "game": game}
        requests.post(WEB_APP_URL, data=json.dumps(payload))
        st.success("Profile saved!")

# 2. Chat Section
st.subheader("Send Message")
sender = st.text_input("Your Name (Sender)")
receiver = st.text_input("Target Name (Receiver)")
msg = st.text_area("Message")
if st.button("Send Message"):
    payload = {"type": "chat", "sender": sender, "receiver": receiver, "message": msg}
    requests.post(WEB_APP_URL, data=json.dumps(payload))
    st.success("Message sent!")
