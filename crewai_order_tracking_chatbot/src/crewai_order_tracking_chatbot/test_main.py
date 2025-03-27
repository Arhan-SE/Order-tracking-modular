
from dotenv import load_dotenv
import os
from crewai_order_tracking_chatbot.crew import order_tracking_chatbot


load_dotenv()

while True:

    query = input(": ")#"Where was order number 936841 going to again?"

    print(f"Starting crew kickoff with query: '{query}'") 

    try:
        crew_object = order_tracking_chatbot()

        response = crew_object.kickoff(inputs={"query": query})

        print("\nCrew finished successfully.")
        print("Response:")
        print(response)

    except Exception as e:
        print(f"\nAn error occurred during crew kickoff: {e}")
        import traceback
        traceback.print_exc() 
    print()
    print("-------------------------")
    print()
