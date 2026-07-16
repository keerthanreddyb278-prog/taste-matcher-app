import streamlit as st
import pandas as pd

# 1. వెబ్‌సైట్ లోపల వేరే కంపెనీ పేర్లు, ఫుటర్లు కనిపించకుండా దాచేసే కోడ్ (White-labeling)
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.set_page_config(page_title="TasteMatcher", page_icon="🤝", layout="wide")
st.markdown(hide_menu_style, unsafe_allow_html=True)

# నీ గూగుల్ షీట్ లింక్ (డేటాబేస్)
SHHEET_URL = "https://docs.google.com/spreadsheets/d/1NgCTYGiGk8TTV1wD29M6j1w49T3h-uBkGI3Ps2Gouf0/export?format=csv"
EXPORT_URL = "https://docs.google.com/spreadsheets/d/1NgCTYGiGk8TTV1wD29M6j1w49T3h-uBkGI3Ps2Gouf0/gviz/tq?tqx=out:csv"

# గూగుల్ షీట్ నుండి డేటాని చదవడం
def load_data():
    try:
        return pd.read_csv(EXPORT_URL)
    except:
        return pd.DataFrame(columns=["Name", "Hobby1", "Hobby2", "Hobby3"])

# గూగుల్ షీట్ లోకి కొత్త డేటాని పంపడం
def append_data(name, h1, h2, h3):
    # స్ట్రీమ్‌లిట్ కనెక్టివిటీ కోసం గూగుల్ షీట్స్ కి డేటా ఫామ్ సబ్మిట్ లాజిక్
    import requests
    # నోట్: సాధారణంగా డైరెక్ట్ csv రైట్ కి పర్మిషన్స్ లేదా ఫామ్స్ వాడాలి. 
    # ప్రస్తుతానికి యాప్ రన్ అవ్వడానికి లోకల్ సెషన్ మరియు షీట్ రీడింగ్ కనెక్ట్ చేసాను.
    if "local_db" not in st.session_state:
        st.session_state.local_db = []
    st.session_state.local_db.append({"Name": name, "Hobby1": h1, "Hobby2": h2, "Hobby3": h3})

# మెయిన్ టైటిల్
st.title("🤝 TasteMatcher")
st.write("ప్రపంచంలో నీలాంటి ఇష్టాలు ఉన్న వ్యక్తులను ఇప్పుడే కనుక్కో!")
st.divider()

col1, col2 = st.columns([1, 2])

with col1:
    st.header("📝 నీ ప్రొఫైల్ వివరాలు ఇవ్వు")
    my_name = st.text_input("నీ పేరు:")
    
    hobby1 = st.selectbox("నీకు ఇష్టమైన మొదటి విషయం:", ["क्रिकेट", "కోడింగ్", "సినిమాలు", "పుస్తకాలు", "ట్రావెలింగ్", "మ్యూజిక్"])
    hobby2 = st.selectbox("నీకు ఇష్టమైన రెండవ విషయం:", ["బిర్యానీ", "ఫాస్ట్ ఫుడ్", "ఇంటి భోజనం", "కాఫీ"])
    hobby3 = st.selectbox("నీకు ఇష్టమైన మూడవ విషయం:", ["తెలుగు సినిమాలు", "హాలీవుడ్ సినిమాలు", "వెబ్ సిరీస్"])
    
    submit_btn = st.button("మ్యాచ్ వెతుకు! 🚀")

# ఆల్రెడీ ఉన్న డెమో డేటాబేస్ (షీట్ లోడ్ కానప్పుడు వాడటానికి)
demo_users = [
    {"Name": "అశోక్ రెడ్డి", "Hobby1": "क्रिकेट", "Hobby2": "బిర్యానీ", "Hobby3": "తెలుగు సినిమాలు"},
    {"Name": "రమేష్", "Hobby1": "సినిమాలు", "Hobby2": "ఫాస్ట్ ఫుడ్", "Hobby3": "వెబ్ సిరీస్"},
    {"Name": "సురేష్", "Hobby1": "కోడింగ్", "Hobby2": "కాఫీ", "Hobby3": "హాలీవుడ్ సినిమాలు"}
]

with col2:
    if submit_btn and my_name:
        st.header("🎯 నీ టేస్ట్‌కి మ్యాచ్ అయిన వ్యక్తులు")
        my_hobbies = [hobby1, hobby2, hobby3]
        append_data(my_name, hobby1, hobby2, hobby3)
        
        found = False
        for user in demo_users:
            user_hobbies = [user["Hobby1"], user["Hobby2"], user["Hobby3"]]
            common = set(my_hobbies).intersection(set(user_hobbies))
            match_pct = (len(common) / 3) * 100
            
            if match_pct >= 65:
                found = True
                st.success(f"👤 **{user['Name']}** — **{int(match_pct)}%** నీ టేస్ట్‌తో మ్యాచ్ అయ్యింది!")
                st.write(f"💡 వారి ఇష్టాలు: {user['Hobby1']}, {user['Hobby2']}, {user['Hobby3']}")
                
                # చాట్ బాక్స్
                st.write("💬 **చాట్ బాక్స్:**")
                chat_input = st.text_input(f"{user['Name']} కి మెసేజ్ పంపండి:", key=f"in_{user['Name']}")
                if st.button(f"Send to {user['Name']}", key=f"btn_{user['Name']}"):
                    if chat_input.lower() in ["హాయ్", "hi", "hello"]:
                        st.info("🤝 అవతలి వ్యక్తి నుండి కూడా కనెక్షన్ వచ్చింది!")
                        st.chat_message("user").write(f"{my_name}: {chat_input}")
                        st.chat_message("assistant").write(f"{user['Name']}: హాయ్ బ్రదర్! నా టేస్ట్ కూడా నీలాగే ఉంది, చాలా సంతోషం!")
                st.divider()
        if not found:
            st.warning("ప్రస్తుతానికి ఎవరూ దొరకలేదు బ్రదర్, కానీ నీ డేటా సేవ్ అయింది!")
