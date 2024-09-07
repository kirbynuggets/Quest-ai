<<<<<<< HEAD
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton
import sys
from backend import Chatbot
import threading


# noinspection PyUnresolvedReferences
class ChatbotWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Instantiate Chatbot class from backend with your Gemini API Key
        self.chatbot = Chatbot("_")

        self.setMinimumSize(700, 500)

        # Add chat area widget
        self.chat_area = QTextEdit(self)
        self.chat_area.setGeometry(10, 10, 480, 320)
        # To set the chat area only readable
        self.chat_area.setReadOnly(True)

        # Add the input field widget
        self.input_area = QLineEdit(self)
        self.input_area.setGeometry(10, 340, 480, 40)
        # To send msg when pressed 'Enter' key on keypad rather than selecting 'Send' button on gui
        self.input_area.returnPressed.connect(self.send_message)

        # Add the button
        self.button = QPushButton("Send", self)
        self.button.setGeometry(500, 340, 80, 40)
        self.button.clicked.connect(self.send_message)

        self.show()

    def send_message(self):
        user_input = self.input_area.text().strip()
        self.chat_area.append(f"<p style='color:#333333'>Me: {user_input}</p>")
        self.input_area.clear()
        # Threading
        thread = threading.Thread(target=self.get_bot_response, args=(user_input, ))
        thread.start()

    def get_bot_response(self, user_input):
        response = self.chatbot.get_response(user_input)
        self.chat_area.append(f"<p style='color:#333333; background-color: #E9E9E9'>Bot: {response}</p>")


app = QApplication(sys.argv)
chatbot_window = ChatbotWindow()
sys.exit(app.exec())
=======
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
>>>>>>> origin/main
