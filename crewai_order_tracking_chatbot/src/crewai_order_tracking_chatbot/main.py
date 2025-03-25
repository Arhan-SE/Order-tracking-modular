
import streamlit as st
from dotenv import load_dotenv
from mem0 import Memory
from openai import OpenAI
import os
import time
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



def check_can_answer(query, context):
    """
    First GPT to check if it can answer based on context
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Your job is to determine if the given context contains enough information to answer the user's query. If you cannot answer based on the context then just say 'i cannot'."},
        {"role": "user", "content": f"Context: {context}\n\nQuery: {query}\n\nCan you answer this query based on the given context?."}
    ]

    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=messages,
    temperature=0)

    return response.choices[0].message.content

def get_answer_from_context(query, context):
    """
    Second GPT to provide the answer using context
    """
    messages = [
        {"role": "system", "content": "You are an Order Tracking Chatbot. Answer the query using the provided context about the tracking details. If you cannot answer then just say 'i cannot'"},
        {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
    ]

    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=messages)

    return response.choices[0].message.content.strip()

def run(query):
    relevant_info=memory.search(query=query, limit=5, user_id="default_user")
    context_lst = [entry["memory"] for entry in relevant_info['results']]
    context = "\n".join(context_lst)
    # context="no context available"
    print()
    print(context)
    print()
    can_answer = check_can_answer(query, context)

    if not can_answer=="i cannot" or can_answer=="i can't":
        print()
        print("can answer")
        print()
        answer = get_answer_from_context(query, context)
        memory.add(f"User Query: {query}\nAI Response: {answer}", user_id="default_user")
        return answer
    else:
        print()
        print("CrewaiOrderTrackingChatbotCrew")
        print()
        inputs = {"query": query}
        response = CrewaiOrderTrackingChatbotCrew().crew().kickoff(inputs=inputs)

        memory.add(f"User Query: {query}\nAI Response: {response}", user_id="default_user")
        return response

if __name__ == "__main__":

    query = "What is the order detail of order number 936848"
    print(run(query))