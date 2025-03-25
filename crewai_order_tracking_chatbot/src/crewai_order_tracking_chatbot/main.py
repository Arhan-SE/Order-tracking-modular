import streamlit as st
from dotenv import load_dotenv
from mem0 import Memory
from openai import OpenAI
import os
from crewai_order_tracking_chatbot.crew import CrewaiOrderTrackingChatbotCrew

load_dotenv()

client = OpenAI()

config = {
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-3.5-turbo",
        },
    },
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
        {"role": "system", "content": "You are an Order Tracking Chatbot. Answer using the given context. If unsure, say 'i cannot'."},  
        {"role": "user", "content": f"Context: {context}\nQuery: {query}"}  
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    return response.choices[0].message.content.strip()

def run(query):
    # Search only 1 most relevant memory entry instead of 3
    relevant_info = memory.search(query=query, limit=1, user_id="default_user")
    context = relevant_info['results'][0]["memory"] if relevant_info['results'] else ""

    # Check if the answer exists in session cache
    if query in st.session_state:
        return st.session_state[query]

    answer = get_answer_from_context(query, context)

    if "i cannot" not in answer.lower():
        memory.add(f"User Query: {query}\nAI Response: {answer}", user_id="default_user")
    else:
        response = CrewaiOrderTrackingChatbotCrew().crew().kickoff(inputs={"query": query})
        answer = response
        memory.add(f"User Query: {query}\nAI Response: {answer}", user_id="default_user")

    st.session_state[query] = answer  # Cache response
    return answer

st.title("Order Tracking Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

if prompt := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = run(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Show only last 5 messages for better performance
for message in st.session_state.messages[-5:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
