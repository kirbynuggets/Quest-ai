import requests

GEMINI_API_KEY = "AIzaSyCRYCMBIJ_k3jrZ-oAP5z6jYscLXYiqThQ"


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
    chatbot = Chatbot("AIzaSyCRYCMBIJ_k3jrZ-oAP5z6jYscLXYiqThQ")
    # Get response
    response = chatbot.get_response("Why temperature is used in chatbot code?")
    print(response)