from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_order_tracking_chatbot.tools.custom_tool import OrderTrackingTool
import os



from dotenv import load_dotenv

load_dotenv()
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
            verbose=False
    )
