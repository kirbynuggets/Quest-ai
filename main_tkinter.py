import sys
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from chatbot_gui_tkinter import ChatbotGUI
from dotenv import load_dotenv

def get_api_key():
    """Get API key from environment or user input"""
    # Try to load from .env file
    load_dotenv()
    api_key = os.getenv('DEEPSEEK_API_KEY')
    
    if api_key:
        return api_key
    
    # If not found, ask user to input
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    api_key = simpledialog.askstring(
        'API Key Required', 
        'Please enter your DeepSeek API key:\n\n'
        'You can get one from: https://platform.deepseek.com/\n\n'
        'This will power Quest-ai with advanced AI capabilities.',
        initialvalue='sk-'
    )
    
    root.destroy()
    
    if not api_key or not api_key.strip():
        messagebox.showerror('Error', 'API key is required to run Quest-ai!')
        sys.exit(1)
    
    return api_key.strip()

def main():
    try:
        print("Starting Quest-ai...")
        
        # Get API key
        print("Getting API key...")
        api_key = get_api_key()
        print(f"API key obtained: {api_key[:10]}...")
        
        # Validate API key format
        if not api_key.startswith('sk-'):
            print("Warning: API key doesn't start with 'sk-'")
            root = tk.Tk()
            root.withdraw()
            messagebox.showwarning('Warning', 'API key should start with "sk-". Please verify your key.')
            root.destroy()
        
        # Create and run the application
        print("Creating ChatbotGUI...")
        app = ChatbotGUI(api_key)
        print("Starting application...")
        app.run()
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror('Error', f'Failed to start Quest-ai: {str(e)}')
            root.destroy()
        except:
            pass
        sys.exit(1)

if __name__ == '__main__':
    main()
