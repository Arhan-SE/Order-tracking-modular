import streamlit as st
from dotenv import load_dotenv
import os
from crewai_order_tracking_chatbot.crew import order_tracking_chatbot

load_dotenv()





def run(query):

    if query in st.session_state:
        return st.session_state[query]

    crew_object = order_tracking_chatbot()

    response = crew_object.kickoff(inputs={"query": query})

    print("\nCrew finished successfully.")
    print()
    print("----------------------")
    print()

    st.session_state[query] = response  
    return response


st.title("📦 Order Tracking Chatbot")
st.caption("Ask me about your order status!")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you track your order today?"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("e.g., Where is order 936850?")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = run(user_input)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Chat history cleared. How can I help?"}
    ]
    st.rerun()

