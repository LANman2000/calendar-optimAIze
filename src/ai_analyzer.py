import json
from typing import Any, Dict, List

class AIAnalyzer:
    """
    Sends parsed calendar events to an AI model and returns optimization suggestions.
    """

    def __init__(self, client):
        """
        client = an instantiated model client with a chat(messages) method.
        """
        self.client = client

    def analyze(self, events: List[Dict[str, Any]]) -> str:
        """
        Sends events to the model and returns a structured weekly optimization plan.
        """
        prompt = self._build_prompt(events)
        return self._send_to_model(prompt)

    def _build_prompt(self, events: List[Dict[str, Any]]) -> str:
        """
        Creates a structured prompt for the model.
        """
        return f"""
You are a schedule optimization assistant.

The user is a busy student balancing classes, gym, sleep, and personal time.
Here is the user's weekly calendar as JSON:

{json.dumps(events, indent=2)}

Your tasks:
1. Identify sleep rhythm issues.
2. Identify overloaded days.
3. Identify free blocks suitable for gym.
4. Suggest a consistent weekly routine.
5. Suggest specific time slots for sleep, gym, meals, and recovery.
6. Return your answer as a structured plan with headings.

Make your suggestions realistic and based on the actual schedule.
"""

    def _send_to_model(self, prompt: str) -> str:
        """
        Sends the prompt to the model using the provided client.
        """
        try:
            response = self.client.chat(
                [{"role": "user", "content": prompt}]
            )
            content = response.choices[0].message.content
            if content is None:
                raise ValueError("AI model returned an empty response.")
            return content

        except Exception as e:
            raise RuntimeError(f"AI model request failed: {e}") from e


# Example usage (optional)
if __name__ == "__main__":
    from model_client import GroqModelClient

    sample_events = [
        {
            "name": "Gym Session",
            "begin": "2026-10-06T18:00:00",
            "end": "2026-10-06T19:00:00",
            "duration_minutes": 60,
            "location": "Fitness Center",
            "description": "Leg day",
        }
    ]
    print(AIAnalyzer(GroqModelClient()).analyze(sample_events))