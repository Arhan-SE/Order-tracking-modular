import streamlit as st
from dotenv import load_dotenv
import os
from crewai_order_tracking_chatbot.custom_mem_crew import order_tracking_chatbot

load_dotenv()


crew_object = order_tracking_chatbot()
query=input(": ")
response = crew_object.kickoff(inputs={"query": query})
print(response)



