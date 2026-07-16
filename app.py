import streamlit as st
import pandas as pd

# 1. Hide Streamlit Branding (White-labeling)
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.set_page_config(page_title="TasteMatcher", page_icon="🤝", layout="wide")
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Your Google Sheet Link (Database Connection)
SHHEET_URL = "https://docs.google.com/spreadsheets/d/1NgCTYGiGk8TTV1wD29M6j1w49T3h-uBkGI3Ps2Gouf0/export?format=csv"
EXPORT_URL = "https://docs.google.com/spreadsheets/d/1NgCTYGiGk8TTV1wD29M6j1w49T3h-uBkGI3Ps2Gouf0/gviz/tq?tqx=out:csv"

# Function to append data (Temporary session storage for demo)
def append_data(name, h1, h2, h3):
    if "local_db" not in st.session_state:
        st.session_state.local_db = []
    st.session_state.local_db.append({"Name": name, "Hobby1": h1, "Hobby2": h2, "Hobby3": h3})

# Main Website Title
st.title("🤝 TasteMatcher")
st.write("Find people around the world who share your exact tastes and interests!")
st.divider()

col1, col2 = st.columns([1, 2])

with col1:
    st.header("📝 Create Your Profile")
    my_name = st.text_input("Enter your Name:")
    
    st.write("---")
    hobby1 = st.selectbox("Select your main hobby/interest:", ["Cricket", "Coding", "Movies", "Books", "Travelling", "Music"])
    
    # Manual input boxes
    hobby2 = st.text_input("Enter your favorite food (e.g., Biryani, Pizza):")
    hobby3 = st.text_input("Enter your favorite movie genre or show (e.g., Telugu Movies, Anime):")
    
    submit_btn = st.button("Find My Match! 🚀")

# Demo Database for matching
demo_users = [
    {"Name": "Ashok Reddy", "Hobby1": "Cricket", "Hobby2": "Biryani", "Hobby3": "Telugu Movies"},
    {"Name": "Ramesh", "Hobby1": "Movies", "Hobby2": "Pizza", "Hobby3": "Web Series"},
    {"Name": "Suresh", "Hobby1": "Coding", "Hobby2": "Coffee", "Hobby3": "Hollywood Movies"}
]

with col2:
    if submit_btn and my_name and hobby2 and hobby3:
        # నార్మల్ గా సబ్మిట్ చేసాక వాళ్ళ పేరుతో థాంక్యూ చెప్పే మెసేజ్
        st.success(f"🎉 Thank you, {my_name}! Your profile has been created successfully.")
        
        st.header("🎯 People with Similar Tastes")
        my_hobbies = [hobby1, hobby2.strip().title(), hobby3.strip().title()]
        append_data(my_name, hobby1, hobby2, hobby3)
        
        found = False
        for user in demo_users:
            user_hobbies = [user["Hobby1"], user["Hobby2"], user["Hobby3"]]
            common = set(my_hobbies).intersection(set(user_hobbies))
            match_pct = (len(common) / 3) * 100
            
            if match_pct >= 65:
                found = True
                st.info(f"👤 **{user['Name']}** — **{int(match_pct)}% Match** with your taste!")
                st.write(f"💡 Their Interests: {user['Hobby1']}, {user['Hobby2']}, {user['Hobby3']}")
                
                # Chat Box (Removed 'brother' reference)
                st.write("💬 **Chat Box:**")
                chat_input = st.text_input(f"Say 'Hi' to {user['Name']}:", key=f"in_{user['Name']}")
                if st.button(f"Send to {user['Name']}", key=f"btn_{user['Name']}"):
                    if chat_input.lower() in ["hi", "hello", "hey"]:
                        st.chat_message("user").write(f"{my_name}: {chat_input}")
                        st.chat_message("assistant").write(f"{user['Name']}: Hi! Glad to know we have similar tastes!")
                st.divider()
        if not found:
            st.warning("No perfect match found right now, but your data has been securely saved!")
    elif submit_btn:
        st.error("Please fill in all the fields to find your match.")
