import streamlit as st
import requests
from datetime import datetime,timedelta,timezone
from dotenv import load_dotenv
import os


load_dotenv()

Query_url = os.getenv("QUERY_URL")

def send_query(query):
    data = {"query": query}
    resp = requests.post(Query_url,json = data)
    return resp.json().get("body")


def display_chats(chats):
     for chat in chats:
        # col1,col2 = st.columns([4,6])
        # with col2:
        with st.chat_message(name = "user"):
            st.markdown(chat["query"])
            st.markdown(f"<span style='font-size: smaller;'>{chat['time']}</span>", unsafe_allow_html=True)

        # c1,c2 = st.columns([10,0])
        # with c1:
        with st.chat_message(name="assistant"):
            st.markdown(chat['response'],unsafe_allow_html=True)
            st.markdown(f"<span style='font-size: smaller;'>{chat['time']}</span>", unsafe_allow_html=True)

def chatbot():
    header = st.container()
    header.title("Chatbot NPS")
    header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

    st.markdown(
        """
    <style>
        div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
            position: fixed;
            top: 2.875rem;
            background-color: white;
            z-index: 999;
            width:100%
        }
        # .fixed-header {
        #     border-bottom: 1px solid black;
        # }
    </style>
        """,
        unsafe_allow_html=True
    )

    chats = st.session_state
    if "history" not in chats:
        chats.history = []
    user_query = st.chat_input("Enter your question here...")
    if user_query != None:
        # current_time = datetime.now().strftime("%H:%M")
        UTC_time = datetime.now(timezone.utc)
        IST_offset = timedelta(hours=5, minutes=30)
        IST_time = UTC_time + IST_offset
        current_time = IST_time.strftime("%H:%M")
        response = send_query(user_query)
        cleaned_response = response.replace("\\n", "<br>").replace("\n", "").replace('"',"")
        chats.history.append({"query": user_query, "response": cleaned_response, "time":current_time})
    
    display_chats(chats.history)

    if len(chats.history)>=10:
        chats.history.pop(0)
        
chatbot()