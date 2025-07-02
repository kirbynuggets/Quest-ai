import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt
from chatbot_gui import ChatbotGUI
from dotenv import load_dotenv

def get_api_key():
    """Get API key from environment or user input"""
    # Try to load from .env file
    load_dotenv()
    api_key = os.getenv('DEEPSEEK_API_KEY')
    
    if api_key:
        return api_key
    
    # If not found, ask user to input
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    api_key, ok = QInputDialog.getText(
        None, 
        'API Key Required', 
        'Please enter your DeepSeek API key:\n\n'
        'You can get one from: https://platform.deepseek.com/\n\n'
        'This will power Quest-ai with advanced AI capabilities.',
        text='sk-'
    )
    
    if not ok or not api_key.strip():
        QMessageBox.critical(None, 'Error', 'API key is required to run Quest-ai!')
        sys.exit(1)
    
    return api_key.strip()

def main():
    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("Quest-ai")
    app.setApplicationVersion("1.0")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Get API key
    try:
        api_key = get_api_key()
    except Exception as e:
        QMessageBox.critical(None, 'Error', f'Failed to get API key: {str(e)}')
        sys.exit(1)
    
    # Validate API key format
    if not api_key.startswith('sk-'):
        QMessageBox.warning(None, 'Warning', 'API key should start with "sk-". Please verify your key.')
    
    # Create and show main window
    try:
        window = ChatbotGUI(api_key)
        window.show()
        
        # Center window on screen
        screen = app.desktop().screenGeometry()
        size = window.geometry()
        window.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
        
    except Exception as e:
        QMessageBox.critical(None, 'Error', f'Failed to create Quest-ai window: {str(e)}')
        sys.exit(1)
    
    # Run application
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()