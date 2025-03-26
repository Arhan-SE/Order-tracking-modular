from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_order_tracking_chatbot.tools.custom_tool import OrderTrackingTool
import os
#from mem0 import MemoryClient
from mem0 import Memory

from dotenv import load_dotenv

load_dotenv()
# client_mem=MemoryClient()

config = {
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "memory",
            "path": "db",
        }
    }
}
m = Memory.from_config(config)
@CrewBase
class CrewaiOrderTrackingChatbotCrew():
    """CrewaiOrderTrackingChatbot crew"""

    @agent
    def order_tracking_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['order_tracking_specialist'],
            tools=[OrderTrackingTool()],
        )


    @task
    def task(self) -> Task:
        return Task(
            config=self.tasks_config['task'],
            tools=[OrderTrackingTool()],
        )




    @crew
    def crew(self) -> Crew:
        """Creates the CrewaiOrderTrackingChatbot crew"""
        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=False,
    #         memory_config={
    #      "provider": "mem0",
    #      "config": {"agent_id": "default_agent"},
    #  },
            memory_config={
                "provider": "mem0",
                "config": {"instance": m, "user_id": "default_user"}, # pass the instance of memory, and a user_id.
            },
    )
