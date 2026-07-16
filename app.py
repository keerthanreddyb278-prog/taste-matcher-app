import streamlit as st
import pandas as pd
import requests
import json

st.set_page_config(page_title="TasteMatcher", page_icon="🤝", layout="wide")

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# ⚠️ IMPORTANT: Paste your NEW Google Web App URL link from Step 1 inside the quotes below
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyXyNV9NjWElpShMAsjmEDNwCARWnMUVzFPGKxkQ0UWKvcEa-M1g6yQUkmkFUNwZF3h8g/exec"

# Google Sheet CSV Links for Profiles (gid=0) and Chats (gid=1040764631)
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
            # 1. Fetch Profiles from Form Responses 1
            df = pd.read_csv(PROFILES_CSV)
            df.columns = ['Timestamp', 'Name', 'Hobby-1', 'Hobby-2', 'Hobby-3']
            
            # 2. Fetch Chat Messages from Sheet2
            try:
                df_chats = pd.read_csv(CHATS_CSV)
                df_chats.columns = ['SENDER', 'RECEIVER', 'MESSAGE', 'TIMESTAMP']
            except:
                df_chats = pd.DataFrame(columns=['SENDER', 'RECEIVER', 'MESSAGE', 'TIMESTAMP'])

            my_hobbies = [hobby1.lower().strip(), hobby2.lower().strip(), hobby3.lower().strip()] if hobby2 else []
            
            found = False
            for index, row in df.iterrows():
                match_name = str(row['Name']).strip()
                if match_name.lower() == my_name.lower().strip():
                    continue
                
                user_hobbies = [str(row['Hobby-1']).lower().strip(), str(row['Hobby-2']).lower().strip(), str(row['Hobby-3']).lower().strip()]
                common = set(my_hobbies).intersection(set(user_hobbies)) if my_hobbies else []
                match_pct = (len(common) / 3) * 100 if my_hobbies else 66
                
                if match_pct >= 65:
                    found = True
                    st.info(f"👤 **{match_name}** — **{int(match_pct)}% Match** with your taste!")
                    st.write(f"💡 Their Interests: {row['Hobby-1']}, {row['Hobby-2']}, {row['Hobby-3']}")
                    
                    st.write("---")
                    current_chats = df_chats[
                        ((df_chats['SENDER'].str.lower() == my_name.lower().strip()) & (df_chats['RECEIVER'].str.lower() == match_name.lower())) |
                        ((df_chats['SENDER'].str.lower() == match_name.lower()) & (df_chats['RECEIVER'].str.lower() == my_name.lower().strip()))
                    ]
                    
                    for c_idx, c_row in current_chats.iterrows():
                        role = "user" if str(c_row['SENDER']).lower() == my_name.lower().strip() else "assistant"
                        st.chat_message(role).write(f"{c_row['SENDER']}: {c_row['MESSAGE']}")
                    
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
