<<<<<<< HEAD
import requests

GEMINI_API_KEY = "_"


class Chatbot:
    def __init__(self, api_key=GEMINI_API_KEY):
        self.api_key = api_key

    def get_response(self, user_input):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {"prompt": user_input, "max_tokens": 4000, "temperature": 0.5}
        response = requests.post("https://api.gemini.ai/v1/completion", headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["text"]


if __name__ == "__main__":
    # Instantiate Chatbot with your Gemini API Key
    chatbot = Chatbot("_")
    # Get response
    response = chatbot.get_response("Why temperature is used in chatbot code?")
    print(response)
=======
import openai
import os

class Chatbot:
    def __init__(self):
        # Load API key from environment variable
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        print(f"API Key: {openai.api_key}")

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
            print(f"Error: {e}")
            return "Sorry, I couldn't process your request."

if __name__ == "__main__":
    chatbot = Chatbot()
    response = chatbot.get_response("Write a joke")
    print(response)
>>>>>>> origin/main
