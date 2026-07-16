import streamlit as st
import pandas as pd
import requests
import json

# --- CONFIGURATION ---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzDCkEKPo2fldOQ-fA-GirKk9AjF5gpIDVeZIGiskTUSIUtwF8YiUSkeXLF2js5Tskruw/exec"
PROFILES_CSV = "https://docs.google.com/spreadsheets/d/1NgCTYGiGk8TTV1wD29M6j1w49T3h-uBkGI3Ps2Gouf0/export?format=csv&gid=2115379032"

# PASTE YOUR CHAT SHEET GID BELOW (Between the quotes)
CHAT_GID = "1040764631" 
CHATS_CSV = f"https://docs.google.com/spreadsheets/d/1NgCTYGiGk8TTV1wD29M6j1w49T3h-uBkGI3Ps2Gouf0/export?format=csv&gid={CHAT_GID}"

st.title("🤝 TasteMatcher Pro")

# 1. Profile Section
my_name = st.text_input("Enter your Name:")
if st.button("Save Profile"):
    requests.post(WEB_APP_URL, data=json.dumps({"type": "profile", "name": my_name}))
    st.success("Profile saved successfully!")

# 2. Match and Chat Section
st.subheader("🎯 Matches & Chat")
try:
    df = pd.read_csv(PROFILES_CSV)
    chats = pd.read_csv(CHATS_CSV)
    
    # Filter for other people
    others = df[df['Name'] != my_name]
    
    for name in others['Name'].unique():
        st.write(f"✅ Chat with {name}:")
        
        # Display existing chat history
        my_chats = chats[(chats['sender'] == name) & (chats['receiver'] == my_name)]
        for m in my_chats['message']:
            st.write(f"💬 {name}: {m}")
            
        # Input to send a new message
        msg = st.chat_input(f"Send message to {name}")
        if msg:
            payload = {"type": "chat", "sender": my_name, "receiver": name, "message": msg}
            requests.post(WEB_APP_URL, data=json.dumps(payload))
            st.rerun() # Refresh to show the new message immediately

except Exception as e:
    st.info("Loading database... Please ensure your Google Sheet is public.")
