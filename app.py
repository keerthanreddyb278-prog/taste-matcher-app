import streamlit as st
import pandas as pd
import requests, json
from streamlit_lottie import st_lottie

# 1. SETUP
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwMVL7Ll_xqn4NUPngdDc7nzPX9JGwA03iIlqSNvq5ulvusmaEFSdPv48y8tLHqXz_reg/exec"
PROFILE_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQAw6ZRGuLMR1wthExoTLZmXC1Y-RA7zE6h1EOYeVKLQv54fQw5XdbHzcMjWxE7636H8ATU9Q7CJdFb/pub?gid=0&single=true&output=csv"
CHAT_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQAw6ZRGuLMR1wthExoTLZmXC1Y-RA7zE6h1EOYeVKLQv54fQw5XdbHzcMjWxE7636H8ATU9Q7CJdFb/pub?gid=573018232&single=true&output=csv"

# Animation Loader
def load_lottieurl(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

lottie_hello = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_jc921b3a.json")

st.title("🤝 TasteMatcher Pro")
st_lottie(lottie_hello, height=200, key="hello")

# 2. Profile Creation
with st.form("profile_setup"):
    name = st.text_input("My Name")
    hobby = st.text_input("My Hobby")
    food = st.text_input("Favorite Food")
    game = st.text_input("Favorite Game")
    if st.form_submit_button("Save Profile"):
        payload = {"type": "profile", "name": name, "hobby": hobby, "food": food, "game": game}
        requests.post(WEB_APP_URL, data=json.dumps(payload))
        st.success(f"Thank you {name}! Your profile is saved.")

# 3. Matching Logic (>85%)
st.subheader("High Compatibility Matches (>85%)")
try:
    df = pd.read_csv(PROFILE_CSV_URL)
    my_hobby = st.text_input("Enter your hobby to find friends:")
    my_food = st.text_input("Enter your favorite food:")
    my_game = st.text_input("Enter your favorite game:")

    if st.button("Find Matches"):
        # Logic: Compare inputs with database
        matches = df[
            (df['Hobby'].str.lower() == my_hobby.lower()) & 
            (df['Food'].str.lower() == my_food.lower()) & 
            (df['Game'].str.lower() == my_game.lower())
        ]
        
        if not matches.empty:
            for idx, row in matches.iterrows():
                if row['Name'] != name:
                    st.write(f"### Match Found: {row['Name']} (Compatibility: 100%)")
                    msg = st.text_input(f"Message for {row['Name']}", key=f"msg_{row['Name']}")
                    if st.button(f"Send Message", key=f"btn_{row['Name']}"):
                        payload = {"type": "chat", "sender": name, "receiver": row['Name'], "message": msg}
                        requests.post(WEB_APP_URL, data=json.dumps(payload))
                        st.success("Message sent!")
        else:
            st.info("No high-compatibility matches found yet.")

    # 4. Inbox
    st.subheader("📩 My Inbox")
    chats = pd.read_csv(CHAT_CSV_URL)
    inbox = chats[chats['receiver'] == name]
    st.table(inbox[['sender', 'message']])

except Exception:
    st.write("Data is loading...")
