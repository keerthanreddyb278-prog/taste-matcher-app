import streamlit as st
import pandas as pd
import requests, json

WEB_APP_URL = "https://docs.google.com/spreadsheets/d/17Nk-bP4lqs9qpaYQisUb6ndI3VGQU3up6YwzpoQTSzA/edit?gid=0#gid=0"

PROFILE_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQAw6ZRGuLMR1wthExoTLZmXC1Y-RA7zE6h1EOYeVKLQv54fQw5XdbHzcMjWxE7636H8ATU9Q7CJdFb/pub?gid=0&single=true&output=csv"
CHAT_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQAw6ZRGuLMR1wthExoTLZmXC1Y-RA7zE6h1EOYeVKLQv54fQw5XdbHzcMjWxE7636H8ATU9Q7CJdFb/pubhtml?gid=573018232&single=true"

st.title("🤝 TasteMatcher Pro")

# Profile Form
with st.form("profile_form"):
    st.subheader("Create Your Profile")
    name = st.text_input("Name")
    hobby = st.text_input("Hobby")
    food = st.text_input("Favorite Food")
    game = st.text_input("Favorite Game")
    
    if st.form_submit_button("Save Profile"):
        payload = {"type": "profile", "name": name, "hobby": hobby, "food": food, "game": game}
        response = requests.post(WEB_APP_URL, data=json.dumps(payload))
        st.success("Profile saved successfully!")

# Search and Chat
st.subheader("Search & Chat")
try:
    df = pd.read_csv(PROFILE_CSV_URL)
    
    # Input for searching
    search_hobby = st.text_input("Enter Hobby to search:")
    search_food = st.text_input("Enter Food to search:")
    search_game = st.text_input("Enter Game to search:")
    
    if st.button("Find Matches"):
        matches = df[
            (df['Hobby'].str.lower() == search_hobby.lower()) & 
            (df['Food'].str.lower() == search_food.lower()) & 
            (df['Game'].str.lower() == search_game.lower())
        ]
        
        if not matches.empty:
            for idx, row in matches.iterrows():
                if row['Name'] != name:
                    st.write(f"### Match Found: {row['Name']}")
                    msg = st.text_input(f"Send message to {row['Name']}", key=f"msg_{row['Name']}")
                    if st.button(f"Send to {row['Name']}", key=f"btn_{row['Name']}"):
                        payload = {"type": "chat", "sender": name, "receiver": row['Name'], "message": msg}
                        requests.post(WEB_APP_URL, data=json.dumps(payload))
                        st.success("Message sent!")
        else:
            st.info("No matches found.")

    # Inbox
    st.subheader("📩 Inbox")
    chats = pd.read_csv(CHAT_CSV_URL)
    my_inbox = chats[chats['receiver'] == name]
    st.table(my_inbox[['sender', 'message']])

except:
    st.write("Data loading... (Make sure your CSV links are correct and public)")
