import streamlit as st
from dotenv import load_dotenv
from mem0 import Memory
from openai import OpenAI
import os
from crewai_order_tracking_chatbot.crew import CrewaiOrderTrackingChatbotCrew

load_dotenv()

client = OpenAI()

config = {
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "chatbot_memory",
            "path": "./chroma_db",
        },
    },
}

memory = Memory.from_config(config)

def get_answer_from_context(query, context):
    messages = [
        {"role": "system", "content": "You are an Order Tracking Chatbot with real-time access to order status. Use the provided context to answer queries accurately. If the information is insufficient, respond with 'i cannot' without guessing."},  
        {"role": "user", "content": f"Context: {context}\nQuery: {query}"}  
    ]

    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=messages)

    return response.choices[0].message.content.strip()

def run(query):
    relevant_info = memory.search(query=query, limit=5, user_id="default_user")
    context_lst = [entry["memory"] for entry in relevant_info['results']]
    context = "\n".join(context_lst)
    
    answer = get_answer_from_context(query, context)

    if "i cannot" not in answer.lower():
        memory.add(f"User Query: {query}\nAI Response: {answer}", user_id="default_user")
        return f"Openai: {answer}"
    else:
        inputs = {"query": query}
        response = CrewaiOrderTrackingChatbotCrew().crew().kickoff(inputs=inputs)
        memory.add(f"User Query: {query}\nAI Response: {response}", user_id="default_user")
        return f"Crewai: {response}"

st.title("Order Tracking Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to know?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = run(prompt)

    st.chat_message("assistant").markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})