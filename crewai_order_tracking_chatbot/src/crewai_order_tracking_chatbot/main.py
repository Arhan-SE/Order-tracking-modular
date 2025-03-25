
from crewai_order_tracking_chatbot.crew import CrewaiOrderTrackingChatbotCrew
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


inputs={
    "query": "What is the order detail of order number 936842"
}

response=CrewaiOrderTrackingChatbotCrew().crew().kickoff(inputs=inputs)
print(response)


import streamlit as st
from dotenv import load_dotenv
from mem0 import Memory
import openai
import os
import time

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY



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

    messages = [
        {"role": "system", "content": "You are a helpful assistant. Your job is to determine if the given context contains enough information to answer the user's query. Respond with only 'yes' or 'no'."},
        {"role": "user", "content": f"Context: {context}\n\nQuery: {query}\n\nCan you answer this query based on the given context? Reply only 'yes' or 'no'."}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0
    )
    
    return response.choices[0].message.content.strip().lower() == 'yes'

def get_answer_from_context(query, context):
    """
    Second GPT to provide the answer using context
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Answer the query using the provided context."},
        {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    return response.choices[0].message.content.strip()
#!/usr/bin/env python
from crewai_order_tracking_chatbot.crew import CrewaiOrderTrackingChatbotCrew
import sys
from dotenv import load_dotenv
import openai
from mem0 import Memory

load_dotenv()
memory = Memory()

def check_can_answer(query, context):
    """
    First GPT to check if it can answer based on context
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Your job is to determine if the given context contains enough information to answer the user's query. Respond with only 'yes' or 'no'."},
        {"role": "user", "content": f"Context: {context}\n\nQuery: {query}\n\nCan you answer this query based on the given context? Reply only 'yes' or 'no'."}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0
    )
    
    return response.choices[0].message.content.strip().lower() == 'yes'

def get_answer_from_context(query, context):
    """
    Second GPT to provide the answer using context
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Answer the query using the provided context."},
        {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    return response.choices[0].message.content.strip()

def run(query):

    context = memory.get_memory()
    

    can_answer = check_can_answer(query, context)
    
    if can_answer:

        answer = get_answer_from_context(query, context)

        memory.add_memory(f"User Query: {query}\nAI Response: {answer}")
        return answer
    else:
        inputs = {"query": query}
        response = CrewaiOrderTrackingChatbotCrew().crew().kickoff(inputs=inputs)

        memory.add_memory(f"User Query: {query}\nAI Response: {response}")
        return response

if __name__ == "__main__":

    query = "What is the order detail of order number 936842"
    print(run(query))