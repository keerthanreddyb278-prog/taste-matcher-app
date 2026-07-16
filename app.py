import streamlit as st
import pandas as pd
import requests
import json

# --- CONFIGURATION ---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzDCkEKPo2fldOQ-fA-GirKk9AjF5gpIDVeZIGiskTUSIUtwF8YiUSkeXLF2js5Tskruw/exec"
PROFILES_CSV = "https://docs.google.com/spreadsheets/d/1NgCTYGiGk8TTV1wD29M6j1w49T3h-uBkGI3Ps2Gouf0/export?format=csv&gid=2115379032"

# PASTE YOUR CHAT SHEET GID HERE
CHAT_GID = "1040764631" 
CHATS_CSV = f"https://docs.google.com/spreadsheets/d/1NgCTYGiGk8TTV1wD29M6j1w49T3h-uBkGI3Ps2Gouf0/export?format=csv&gid={CHAT_GID}"

st.title("🤝 TasteMatcher Pro")

# 1. Detailed Profile Section
st.subheader("Create Your Profile")
my_name = st.text_input("Name:")
hobby = st.text_input("Hobby:")
food = st.text_input("Favorite Food:")
game = st.text_input("Favorite Game:")

if st.button("Save Profile"):
    payload = {"type": "profile", "name": my_name, "hobby": hobby, "food": food, "game": game}
    requests.post(WEB_APP_URL, data=json.dumps(payload))
    st.success("Profile saved!")

# 2. Match and Chat Section
st.subheader("🎯 Matches & Chat")
try:
    df = pd.read_csv(PROFILES_CSV)
    chats = pd.read_csv(CHATS_CSV)
    
    # Filter for others
    others = df[df['Name'] != my_name]
    
    for index, row in others.iterrows():
        st.write(f"### ✅ Match: {row['Name']}")
        st.write(f"**Interests:** {row['Hobby']} | **Food:** {row['Food']} | **Game:** {row['Game']}")
        
        # Display chat history
        my_chats = chats[(chats['sender'] == row['Name']) & (chats['receiver'] == my_name)]
        for m in my_chats['message']:
            st.write(f"💬 {row['Name']}: {m}")
            
        # Send message
        msg = st.chat_input(f"Send message to {row['Name']}", key=f"chat_{index}")
        if msg:
            payload = {"type": "chat", "sender": my_name, "receiver": row['Name'], "message": msg}
            requests.post(WEB_APP_URL, data=json.dumps(payload))
            st.rerun()

except Exception as e:
    st.info("Loading database... Ensure your sheet has columns: Name, Hobby, Food, Game.")
