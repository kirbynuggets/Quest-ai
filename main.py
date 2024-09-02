import openai
import os
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Load API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

class Chatbot:
    def __init__(self):
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

    def get_response(self, user_input):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_input}],
                max_tokens=150,  # Adjusted max_tokens
                temperature=0.5
            ).choices[0].message['content'].strip()
            return response
        except Exception as e:
            logging.error(f"Error: {e}")
            return "Sorry, I couldn't process your request."

if __name__ == "__main__":
    chatbot = Chatbot()
    response = chatbot.get_response("Write a joke")
    print(response)
