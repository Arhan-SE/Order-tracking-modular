#!/usr/bin/env python
from crewai_order_tracking_chatbot.crew import CrewaiOrderTrackingChatbotCrew
import sys
from dotenv import load_dotenv

load_dotenv()


def run():
    """
    Run the crew.
    """
    inputs = {
        "query": "What is the order detail of order number 936842"
    }
    CrewaiOrderTrackingChatbotCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "query": "What is the order detail of order number 936842"
    }
    try:
        CrewaiOrderTrackingChatbotCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CrewaiOrderTrackingChatbotCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "query": "What is the order detail of order number 936842"
    }
    try:
        CrewaiOrderTrackingChatbotCrew().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py <command> [<args>]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        run()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
