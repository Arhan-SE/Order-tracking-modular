import streamlit as st
from dotenv import load_dotenv
# from mem0 import Memory
from openai import OpenAI
import os
from crewai_order_tracking_chatbot.crew import CrewaiOrderTrackingChatbotCrew

load_dotenv()

client = OpenAI()

# config = {
#     "llm": {
#         "provider": "openai",
#         "config": {
#             "model": "gpt-3.5-turbo",
#         },
#     },
#     "vector_store": {
#         "provider": "chroma",
#         "config": {
#             "collection_name": "chatbot_memory",
#             "path": "./chroma_db",
#         },
#     },
# }

# memory = Memory.from_config(config)

# def get_answer_from_context(query, context):
#     messages = [
#         {"role": "system", "content": "You are an Order Tracking Chatbot. Answer using the given context. If unsure, say 'i cannot'."},  
#         {"role": "user", "content": f"Context: {context}\nQuery: {query}"}  
#     ]

#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=messages
#     )

#     return response.choices[0].message.content.strip()

def run(query):
    # relevant_info = memory.search(query=query, limit=1, user_id="default_user")
    # context = relevant_info['results'][0]["memory"] if relevant_info['results'] else ""

    # if query in st.session_state:
    #     return st.session_state[query]

    # answer = get_answer_from_context(query, context)

    # if "i cannot" not in answer.lower():
    #     memory.add(f"User Query: {query}\nAI Response: {answer}", user_id="default_user")
    # else:
    response = CrewaiOrderTrackingChatbotCrew().crew().kickoff(inputs={"query": query})
    # answer = response
    #memory.add(f"User Query: {query}\nAI Response: {answer}", user_id="default_user")

    # st.session_state[query] = answer  
    return response

responses=run("Tell me the details of order number")
print(responses)