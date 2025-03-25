
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
        {"role": "system", "content": "You are a helpful assistant. Your job is to determine if the given context contains enough information to answer the user's query. Respond with only 'yes' or 'no'."},
        {"role": "user", "content": f"Context: {context}\n\nQuery: {query}\n\nCan you answer this query based on the given context? Reply only 'yes' or 'no'."}
    ]

    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=messages,
    temperature=0)

    return response.choices[0].message.content.strip().lower() == 'yes'

def get_answer_from_context(query, context):
    """
    Second GPT to provide the answer using context
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Answer the query using the provided context."},
        {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
    ]

    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=messages)

    return response.choices[0].message.content.strip()

def run(query):
    relevant_info=memory.search(query=query, limit=10, user_id="default_user")
    context="\n".join(msg.get("memory", "") for msg in relevant_info if isinstance(msg, dict))
    # context="no context available"

    can_answer = check_can_answer(query, context)

    if can_answer:
        print()
        print("can answer")
        print()
        answer = get_answer_from_context(query, context)

        memory.add_memory(f"User Query: {query}\nAI Response: {answer}", user_id="default_user")
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