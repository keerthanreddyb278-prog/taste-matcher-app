import streamlit as st
import pandas as pd
import requests
import json

st.set_page_config(page_title="TasteMatcher", page_icon="🤝", layout="wide")

# Hide Streamlit Branding
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# ⚠️ IMPORTANT: Paste your new Google Web App URL link inside the quotes below
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyxSigBa9tUdXeg-tp0weXa5jdGbo1L5TdDQElC0D7-5yl3bK0wcta49csVzT0OJiyY8A/exec"

# Google Sheet CSV Link to read REAL data
GOOGLE_SHEET_CSV = "https://docs.google.com/spreadsheets/d/1NgCTYGiGk8TTV1wD29M6j1w49T3h-uBkGI3Ps2Gouf0/export?format=csv&gid=1040764631"

# Function to send profile data to Google Sheet
def send_profile_to_sheet(name, h1, h2, h3):
    payload = {"type": "profile", "name": name, "h1": h1, "h2": h2, "h3": h3}
    try: 
        requests.post(WEB_APP_URL, data=json.dumps(payload))
    except: 
        pass

# Function to send chat messages to Google Sheet
def send_message_to_sheet(sender, receiver, message):
    payload = {"type": "chat", "sender": sender, "receiver": receiver, "message": message}
    try: 
        requests.post(WEB_APP_URL, data=json.dumps(payload))
    except: 
        pass

# Main Interface
st.title("🤝 TasteMatcher (Live Chat)")
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
    if my_name:
        if submit_btn and hobby2 and hobby3:
            send_profile_to_sheet(my_name, hobby1, hobby2.strip(), hobby3.strip())
            st.success(f"🎉 Profile Updated successfully, {my_name}!")
        
        st.header("🎯 Real People with Similar Tastes")
        try:
            # 1. Fetch Profiles from Google Sheet
            df = pd.read_csv("https://docs.google.com/spreadsheets/d/1NgCTYGiGk8TTV1wD29M6j1w49T3h-uBkGI3Ps2Gouf0/export?format=csv&gid=0")
            df.columns = ['Timestamp', 'Name', 'Hobby-1', 'Hobby-2', 'Hobby-3']
            
            # 2. Fetch Chat Messages from Sheet2
            try:
                df_chats = pd.read_csv(GOOGLE_SHEET_CSV)
                df_chats.columns = ['SENDER', 'RECEIVER', 'MESSAGE', 'TIMESTAMP']
            except:
                df_chats = pd.DataFrame(columns=['SENDER', 'RECEIVER', 'MESSAGE', 'TIMESTAMP'])

            my_hobbies = [hobby1.lower().strip(), hobby2.lower().strip(), hobby3.lower().strip()] if hobby2 else []
            
            found = False
            for index, row in df.iterrows():
                match_name = str(row['Name']).strip()
                # Skip matching with oneself
                if match_name.lower() == my_name.lower().strip():
                    continue
                
                # Real-time data matching logic
                user_hobbies = [str(row['Hobby-1']).lower().strip(), str(row['Hobby-2']).lower().strip(), str(row['Hobby-3']).lower().strip()]
                common = set(my_hobbies).intersection(set(user_hobbies)) if my_hobbies else []
                match_pct = (len(common) / 3) * 100 if my_hobbies else 66  # Default fallback match %
                
                if match_pct >= 65:
                    found = True
                    st.info(f"👤 **{match_name}** — **{int(match_pct)}% Match** with your taste!")
                    st.write(f"💡 Their Interests: {row['Hobby-1']}, {row['Hobby-2']}, {row['Hobby-3']}")
                    
                    # 💬 Display history of chat between these two specific users from Google Sheet
                    st.write("---")
                    current_chats = df_chats[
                        ((df_chats['SENDER'].str.lower() == my_name.lower().strip()) & (df_chats['RECEIVER'].str.lower() == match_name.lower())) |
                        ((df_chats['SENDER'].str.lower() == match_name.lower()) & (df_chats['RECEIVER'].str.lower() == my_name.lower().strip()))
                    ]
                    
                    for c_idx, c_row in current_chats.iterrows():
                        role = "user" if str(c_row['SENDER']).lower() == my_name.lower().strip() else "assistant"
                        st.chat_message(role).write(f"{c_row['SENDER']}: {c_row['MESSAGE']}")
                    
                    # Text input to send message
                    chat_input = st.text_input(f"Type message to {match_name}:", key=f"in_{match_name}")
                    if st.button(f"Send to {match_name}", key=f"btn_{match_name}"):
                        if chat_input:
                            send_message_to_sheet(my_name, match_name, chat_input)
                            st.success("Message sent! Refreshing screen...")
                            st.rerun()
                    st.divider()
            if not found:
                st.warning("No real-time matches found from the database yet.")
        except Exception as e:
            st.error("Connecting to live database... Please click 'Find My Match' after updating your profile details.")
