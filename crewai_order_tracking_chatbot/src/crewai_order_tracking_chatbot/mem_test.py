import streamlit as st
from dotenv import load_dotenv
import os
from crewai_order_tracking_chatbot.crew import CrewaiOrderTrackingChatbotCrew

load_dotenv()

def run(query):
    crew_instance = CrewaiOrderTrackingChatbotCrew()
    crew_object = crew_instance.crew()

    response = crew_object.kickoff(inputs={"query": query})

    print("\nCrew finished successfully.")
    print()
    print("----------------------")
    print()
    return response

query="Tell me the details of order number 936841" #Where was order number 936841 going to again?
response = run(query)
print()
print(response)
print("---------------")
print()