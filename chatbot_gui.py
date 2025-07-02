import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from deepseek_api import DeepSeekAPI
import threading

class MessageWidget(QWidget):
    def __init__(self, message, is_user=True):
        super().__init__()
        self.is_user = is_user
        self.init_ui(message)
    
    def init_ui(self, message):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Message bubble
        bubble = QLabel()
        bubble.setWordWrap(True)
        bubble.setText(message)
        bubble.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        # Styling
        if self.is_user:
            bubble.setStyleSheet("""
                QLabel {
                    background-color: #007acc;
                    color: white;
                    padding: 12px 16px;
                    border-radius: 18px;
                    font-size: 14px;
                    max-width: 300px;
                }
            """)
            layout.addStretch()
            layout.addWidget(bubble)
        else:
            bubble.setStyleSheet("""
                QLabel {
                    background-color: #f1f3f5;
                    color: #333;
                    padding: 12px 16px;
                    border-radius: 18px;
                    font-size: 14px;
                    max-width: 400px;
                    border: 1px solid #e9ecef;
                }
            """)
            layout.addWidget(bubble)
            layout.addStretch()
        
        self.setLayout(layout)

class ChatbotGUI(QMainWindow):
    def __init__(self, api_key):
        super().__init__()
        self.api = DeepSeekAPI(api_key)
        self.init_ui()
        
        # Default system prompt
        self.system_prompt = "You are a helpful AI assistant. Be concise, friendly, and informative in your responses."
    
    def init_ui(self):
        self.setWindowTitle("Quest-ai")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(600, 400)
        
        # Set application icon (you can add an icon file)
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        self.create_header(main_layout)
        
        # Chat area
        self.create_chat_area(main_layout)
        
        # Input area
        self.create_input_area(main_layout)
        
        # Status bar
        self.statusBar().showMessage("Ready to chat!")
        
        # Apply modern styling
        self.apply_styles()
        
        # Welcome message
        self.add_message("Hello! I'm Quest-ai, your intelligent AI assistant powered by DeepSeek AI. How can I help you today?", False)
    
    def create_header(self, parent_layout):
        header = QWidget()
        header.setFixedHeight(60)
        header.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-bottom: 1px solid #ddd;
            }
        """)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        # Title
        title = QLabel("Quest-ai")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
                background: transparent;
            }
        """)
        
        # Clear button
        clear_btn = QPushButton("Clear Chat")
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                padding: 8px 16px;
                border-radius: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        clear_btn.clicked.connect(self.clear_chat)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(clear_btn)
        
        parent_layout.addWidget(header)
    
    def create_chat_area(self, parent_layout):
        # Scroll area for messages
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #ffffff;
            }
            QScrollBar:vertical {
                background-color: #f8f9fa;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #dee2e6;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #adb5bd;
            }
        """)
        
        # Messages container
        self.messages_widget = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_widget)
        self.messages_layout.setContentsMargins(0, 10, 0, 10)
        self.messages_layout.setSpacing(8)
        self.messages_layout.addStretch()
        
        scroll_area.setWidget(self.messages_widget)
        parent_layout.addWidget(scroll_area)
        
        self.scroll_area = scroll_area
    
    def create_input_area(self, parent_layout):
        input_container = QWidget()
        input_container.setFixedHeight(80)
        input_container.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-top: 1px solid #dee2e6;
            }
        """)
        
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(20, 15, 20, 15)
        input_layout.setSpacing(15)
        
        # Input field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your message here...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                padding: 12px 16px;
                border: 2px solid #e9ecef;
                border-radius: 25px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #007acc;
                outline: none;
            }
        """)
        self.input_field.returnPressed.connect(self.send_message)
        
        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.setFixedSize(80, 50)
        self.send_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a6fd8, stop:1 #6a4190);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4d5bc9, stop:1 #5d3a85);
            }
            QPushButton:disabled {
                background-color: #adb5bd;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        
        parent_layout.addWidget(input_container)
    
    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QStatusBar {
                background-color: #f8f9fa;
                color: #6c757d;
                border-top: 1px solid #dee2e6;
            }
        """)
    
    def add_message(self, message, is_user=True):
        message_widget = MessageWidget(message, is_user)
        self.messages_layout.insertWidget(self.messages_layout.count() - 1, message_widget)
        
        # Auto-scroll to bottom
        QTimer.singleShot(50, self.scroll_to_bottom)
    
    def scroll_to_bottom(self):
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def send_message(self):
        message = self.input_field.text().strip()
        if not message:
            return
        
        # Add user message
        self.add_message(message, True)
        self.input_field.clear()
        
        # Disable input while processing
        self.input_field.setEnabled(False)
        self.send_button.setEnabled(False)
        self.statusBar().showMessage("AI is thinking...")
        
        # Send to API in separate thread
        def api_call():
            response = self.api.send_message(message, self.system_prompt)
            
            # Update UI in main thread
            QTimer.singleShot(0, lambda: self.handle_response(response))
        
        thread = threading.Thread(target=api_call)
        thread.daemon = True
        thread.start()
    
    def handle_response(self, response):
        # Add AI response
        self.add_message(response, False)
        
        # Re-enable input
        self.input_field.setEnabled(True)
        self.send_button.setEnabled(True)
        self.input_field.setFocus()
        self.statusBar().showMessage("Ready to chat!")
    
    def clear_chat(self):
        # Clear API conversation history
        self.api.clear_history()
        
        # Clear UI messages
        for i in reversed(range(self.messages_layout.count() - 1)):
            child = self.messages_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # Add welcome message
        self.add_message("Chat cleared! How can I help you?", False)
        self.statusBar().showMessage("Chat cleared - Ready for new conversation!")
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit Confirmation', 
                                   "Are you sure you want to exit?",
                                   QMessageBox.Yes | QMessageBox.No, 
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()