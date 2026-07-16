import streamlit as st
import pandas as pd
import requests, json

# 1. Paste your 3 links here
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwMVL7Ll_xqn4NUPngdDc7nzPX9JGwA03iIlqSNvq5ulvusmaEFSdPv48y8tLHqXz_reg/exec"
PROFILE_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQAw6ZRGuLMR1wthExoTLZmXC1Y-RA7zE6h1EOYeVKLQv54fQw5XdbHzcMjWxE7636H8ATU9Q7CJdFb/pub?gid=0&single=true&output=csv"
CHAT_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQAw6ZRGuLMR1wthExoTLZmXC1Y-RA7zE6h1EOYeVKLQv54fQw5XdbHzcMjWxE7636H8ATU9Q7CJdFb/pub?gid=573018232&single=true&output=csv"

st.title("🤝 TasteMatcher Pro")

# 2. Profile Creation
with st.form("profile_setup"):
    st.subheader("Create Your Profile")
    name = st.text_input("Name")
    hobby = st.text_input("Hobby")
    food = st.text_input("Favorite Food")
    game = st.text_input("Favorite Game")
    
    if st.form_submit_button("Save Profile"):
        payload = {"type": "profile", "name": name, "hobby": hobby, "food": food, "game": game}
        requests.post(WEB_APP_URL, data=json.dumps(payload))
        st.success(f"Profile saved for {name}!")

# 3. Matching Logic
st.subheader("Find Friends with Similar Interests")
try:
    df = pd.read_csv(PROFILE_CSV_URL)
    my_hobby = st.text_input("Enter your hobby:")
    my_food = st.text_input("Enter your favorite food:")
    my_game = st.text_input("Enter your favorite game:")

    if st.button("Find Matches"):
        # Match only if all 3 fields match
        matches = df[
            (df['Hobby'].str.lower() == my_hobby.lower()) & 
            (df['Food'].str.lower() == my_food.lower()) & 
            (df['Game'].str.lower() == my_game.lower())
        ]
        
        if not matches.empty:
            for idx, row in matches.iterrows():
                if row['Name'] != name:
                    st.write(f"### Match Found: {row['Name']}")
                    msg = st.text_input(f"Send message to {row['Name']}", key=f"msg_{row['Name']}")
                    if st.button(f"Send to {row['Name']}", key=f"btn_{row['Name']}"):
                        payload = {"type": "chat", "sender": name, "receiver": row['Name'], "message": msg}
                        requests.post(WEB_APP_URL, data=json.dumps(payload))
                        st.success("Message sent successfully!")
        else:
            st.info("No perfect matches found yet.")

    # 4. Inbox
    st.subheader("📩 My Inbox")
    chats = pd.read_csv(CHAT_CSV_URL)
    my_inbox = chats[chats['receiver'] == name]
    st.table(my_inbox[['sender', 'message']])

except Exception:
    st.write("Loading data... Please ensure your Google Sheet links are public.")
