import requests
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv\
    
load_dotenv()
CLIENT_API_KEY = os.getenv("CLIENT_API_KEY")
CLIENT_API_URL = os.getenv("CLIENT_API_URL")

class OrderTrackingInput(BaseModel):
    """Schema for tracking order input."""
    booking_number: str = Field(..., description="Booking number for the order.")

class OrderTrackingTool(BaseTool):
    name: str = "Order Tracking Tool"
    description: str = "Fetches real-time order tracking details using a booking number."
    args_schema: Type[BaseModel] = OrderTrackingInput

    def _run(self, booking_number: str) -> str:
        response = requests.post(CLIENT_API_URL, json={"booking_number": booking_number}, headers={"apikey": CLIENT_API_KEY})
        return response.json().get("data")

