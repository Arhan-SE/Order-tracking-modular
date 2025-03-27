from crewai import Agent, Task, Crew, Process
from crewai_order_tracking_chatbot.tools.custom_tool import OrderTrackingTool
from mem0 import Memory

prompt="""You are an AI assistant specializing in answering queries about Pinas Cargo. Your knowledge comes from the latest posts stored in memory, which include updates on pricing, delivery areas, promotions, and other relevant details.

When a user asks a question, first check the memory for relevant information and respond accordingly. If the answer is not found in memory, politely inform the user that you don’t have the latest details.

Always provide accurate, up-to-date responses based on the stored data. Do not make assumptions or fabricate information beyond what is available in memory."""

config = {
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "memory",
            "path": "db",
        }
    },
    "custom_instructions": prompt
}

m = Memory.from_config(config)



def order_tracking_chatbot():
    order_tracking_specialist = Agent(
        role="Order Tracking Specialist",
        goal="Extract the tracking ID from user input, fetch the order status, and generate a professional, context-aware response for the user's query.",
        backstory="As an advanced Order Tracking Specialist, you have access to real-time delivery data and tracking information. Your expertise lies in efficiently retrieving order statuses, handling customer queries with precision, and ensuring a smooth tracking experience. You provide clear, concise, and helpful responses based on the latest tracking updates.",
        verbose=True,
        tools=[OrderTrackingTool()],
        memory=True,
    )

    order_tracking_task = Task(
        description="""
        Your task is to assist customers with order tracking inquiries by leveraging the custom tool. Follow these steps:

        1. Extract the `tracking_id` or 'order number' from the user's query {query}.
        2. Call the tool with the extracted `tracking_id` or 'order number' to retrieve real-time tracking details.
        3. Interpret the response and generate a clear, concise, and helpful reply that informs the user about their order status.
        4. If the user asks something about the earlier conversation, use the memories using the memory tool.
        Ensure responses are professional, relevant, and directly answer the user's query.
        """,
        expected_output="The expected output should be a well-structured sentence that directly answers the user's query using the retrieved tracking details.",
        agent=order_tracking_specialist,
        memory=True,
        tools=[OrderTrackingTool()],
    )

    crew = Crew(
        agents=[order_tracking_specialist],
        tasks=[order_tracking_task],
        process=Process.sequential,
        verbose=False,
        memory_config={
            "provider": "mem0",
            "config": {"instance": m, "user_id": "default_user", "custom_instructions": prompt}, # pass the instance of memory, and a user_id.
        },
    )
    return crew
