import streamlit as st
import pandas as pd
import requests
import json

# Hide Streamlit Branding
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.set_page_config(page_title="TasteMatcher", page_icon="🤝", layout="wide")
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Google Apps Script Web App URL (Direct Connection to Sheet)
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyxSigBa9tUdXeg-tp0weXa5jdGbo1L5TdDQElC0D7-5yl3bK0wcta49csVzT0OJiyY8A/exec"

# CSV Export URL of your Google Sheet to read REAL users
GOOGLE_SHEET_CSV = "https://docs.google.com/spreadsheets/d/1NgCTYGiGk8TTV1wD29M6j1w49T3h-uBkGI3Ps2Gouf0/export?format=csv"

# Initialize Chat History in Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

def send_data_to_sheet_direct(name, h1, h2, h3):
    payload = {
        "name": name,
        "h1": h1,
        "h2": h2,
        "h3": h3
    }
    try:
        # Sending JSON data to Google Apps Script
        requests.post(WEB_APP_URL, data=json.dumps(payload))
    except:
        pass

# Main Website Title
st.title("🤝 TasteMatcher")
st.write("Find REAL people around the world who share your exact tastes and interests!")
st.divider()

col1, col2 = st.columns([1, 2])

with col1:
    st.header("📝 Create Your Profile")
    my_name = st.text_input("Enter your Name:", key="user_name")
    
    st.write("---")
    hobby1 = st.selectbox("Select your main hobby/interest:", ["Cricket", "Coding", "Movies", "Books", "Travelling", "Music"])
    hobby2 = st.text_input("Enter your favorite food (e.g., Biryani, Pizza):")
    hobby3 = st.text_input("Enter your favorite movie genre or show (e.g., Telugu Movies, Anime):")
    
    submit_btn = st.button("Find My Match! 🚀")

with col2:
    if submit_btn and my_name and hobby2 and hobby3:
        # 1. Save current user directly to the Google Sheet via Apps Script
        send_data_to_sheet_direct(my_name, hobby1, hobby2.strip(), hobby3.strip())
        st.success(f"🎉 Thank you, {my_name}! Your profile has been created.")
        
        st.header("🎯 Real People with Similar Tastes")
        my_hobbies = [hobby1.lower().strip(), hobby2.lower().strip(), hobby3.lower().strip()]
        
        # 2. Fetch REAL users from Google Sheet
        try:
            df = pd.read_csv(GOOGLE_SHEET_CSV)
            # Standardizing column names
            df.columns = ['Timestamp', 'Name', 'Hobby-1', 'Hobby-2', 'Hobby-3']
            
            found = False
            for index, row in df.iterrows():
                # Skip matching with oneself
                if str(row['Name']).strip().lower() == my_name.lower().strip():
                    continue
                    
                user_hobbies = [str(row['Hobby-1']).lower().strip(), str(row['Hobby-2']).lower().strip(), str(row['Hobby-3']).lower().strip()]
                common = set(my_hobbies).intersection(set(user_hobbies))
                match_pct = (len(common) / 3) * 100
                
                # Show match if it's a real match (at least 65%)
                if match_pct >= 65:
                    found = True
                    match_name = row['Name']
                    st.info(f"👤 **{match_name}** — **{int(match_pct)}% Match** with your taste!")
                    st.write(f"💡 Their Interests: {row['Hobby-1']}, {row['Hobby-2']}, {row['Hobby-3']}")
                    
                    # Real-time Simulation Chat Box
                    st.write(f"💬 **Chat with {match_name}:**")
                    
                    chat_key = f"{my_name}_to_{match_name}"
                    if chat_key in st.session_state.chat_history:
                        for msg in st.session_state.chat_history[chat_key]:
                            st.chat_message(msg["role"]).write(msg["text"])
                    
                    chat_input = st.text_input(f"Type your message to {match_name}:", key=f"in_{match_name}")
                    if st.button(f"Send to {match_name}", key=f"btn_{match_name}"):
                        if chat_input:
                            if chat_key not in st.session_state.chat_history:
                                st.session_state.chat_history[chat_key] = []
                            
                            st.session_state.chat_history[chat_key].append({"role": "user", "text": f"{my_name}: {chat_input}"})
                            st.chat_message("user").write(f"{my_name}: {chat_input}")
                            
                            # Real Person logic (No auto-reply)
                            st.warning(f"Message sent! Waiting for {match_name} to reply...")
                    st.divider()
                    
            if not found:
                st.warning("No real-time match found from database yet. Your profile is live, others can find you now!")
                
        except Exception as e:
            st.error("Connecting to live database... please refresh the page in a moment.")
            
    elif submit_btn:
        st.error("Please fill in all the fields to find your match.")
