import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class GroqModelClient:
    """
    Cloud client for Groq-hosted LLaMA-3 or other open-source models.
    """

    def __init__(self):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Missing GROQ_API_KEY in environment variables.")

        self.model_name = os.environ.get("AI_MODEL_NAME")
        if not self.model_name:
            raise ValueError("Missing AI_MODEL_NAME in environment variables.")

        self.client = Groq(api_key=api_key)

    def chat(self, messages):
        """
        Sends chat messages to Groq's hosted model.
        """
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages
        )
        return response
