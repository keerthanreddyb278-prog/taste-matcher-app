import streamlit as st
import pandas as pd
import requests, json

# Paste your actual URLs here
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxS4cMTM1QxpBxDDBBbns_0DnZUcsSiAIqbFbAFURGkUacCfihp3p85qfB_b0omiGvI9A/exec"
PROFILE_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT62kQ0g6TJA9IrN2nxq3TSumE90Fkj5wwgoOV-0kQjxPUkU4lSz_gW5BdnCLxpwAJ2tw9Q1FlDiNxB/pub?gid=0&single=true&output=csv"
CHAT_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT62kQ0g6TJA9IrN2nxq3TSumE90Fkj5wwgoOV-0kQjxPUkU4lSz_gW5BdnCLxpwAJ2tw9Q1FlDiNxB/pub?gid=1287747295&single=true&output=csv"

st.title("🤝 Private Connect App")

# 1. Profile Creation
with st.form("profile_setup"):
    name = st.text_input("My Name")
    hobby = st.text_input("My Hobby")
    submit_btn = st.form_submit_button("Save Profile")
    
    if submit_btn:
        payload = {"type": "profile", "name": name, "hobby": hobby, "food": "N/A", "game": "N/A"}
        requests.post(WEB_APP_URL, data=json.dumps(payload))
        # Thank you message with name
        st.success(f"Thank you, {name}! Your profile has been saved.")

# 2. Matching and Messaging
st.subheader("Find People with Similar Hobbies")
try:
    # Read profiles from CSV
    profiles = pd.read_csv(PROFILE_CSV_URL)
    my_hobby = st.text_input("Enter your hobby to find matches:")
    
    if my_hobby:
        matches = profiles[profiles['Hobby'].str.contains(my_hobby, case=False, na=False)]
        for index, row in matches.iterrows():
            if row['Name'] != name: # Hide yourself
                st.write(f"### Match Found: {row['Name']}")
                
                # Chat logic
                msg = st.text_input(f"Send message to {row['Name']}", key=f"msg_{row['Name']}")
                if st.button(f"Send to {row['Name']}", key=f"btn_{row['Name']}"):
                    payload = {"type": "chat", "sender": name, "receiver": row['Name'], "message": msg}
                    requests.post(WEB_APP_URL, data=json.dumps(payload))
                    st.success(f"Message sent to {row['Name']}!")

    # 3. View Messages Received
    st.subheader("My Inbox")
    all_chats = pd.read_csv(CHAT_CSV_URL)
    # Filter chats where the user is the receiver
    my_inbox = all_chats[all_chats['receiver'] == name]
    st.table(my_inbox[['sender', 'message']])

except Exception:
    st.info("Profiles/Messages will appear here once you save and link the data.")     
