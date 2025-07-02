import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from deepseek_api import DeepSeekAPI

class ChatbotGUI:
    def __init__(self, api_key):
        self.api = DeepSeekAPI(api_key)
        self.system_prompt = "You are a helpful AI assistant. Be concise, friendly, and informative in your responses."
        self.setup_ui()
        
    def setup_ui(self):
        # Create main window
        self.root = tk.Tk()
        self.root.title("Quest-ai")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Create header frame
        header_frame = tk.Frame(self.root, bg='#667eea', height=60)
        header_frame.pack(fill='x', side='top')
        header_frame.pack_propagate(False)
        
        # Title label
        title_label = tk.Label(header_frame, text="Quest-ai", 
                              font=('Arial', 20, 'bold'), 
                              fg='white', bg='#667eea')
        title_label.pack(side='left', padx=20, pady=15)
        
        # Clear button
        clear_btn = tk.Button(header_frame, text="Clear Chat",
                             font=('Arial', 10, 'bold'),
                             fg='white', bg='#5a6fd8',
                             border=0, relief='flat',
                             activebackground='#4d5bc9',
                             activeforeground='white',
                             command=self.clear_chat)
        clear_btn.pack(side='right', padx=20, pady=15)
        
        # Create chat area
        chat_frame = tk.Frame(self.root, bg='white')
        chat_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, 
            wrap=tk.WORD, 
            state='disabled',
            font=('Arial', 11),
            bg='white',
            fg='#333333'
        )
        self.chat_display.pack(fill='both', expand=True, pady=(0, 10))
        
        # Configure text tags for styling
        self.chat_display.tag_configure("user", foreground="#007acc", font=('Arial', 11, 'bold'))
        self.chat_display.tag_configure("assistant", foreground="#333333", font=('Arial', 11))
        self.chat_display.tag_configure("system", foreground="#666666", font=('Arial', 10, 'italic'))
        
        # Create input area
        input_frame = tk.Frame(self.root, bg='#f8f9fa', height=80)
        input_frame.pack(fill='x', side='bottom')
        input_frame.pack_propagate(False)
        
        # Input field and send button frame
        input_controls = tk.Frame(input_frame, bg='#f8f9fa')
        input_controls.pack(fill='x', padx=20, pady=15)
        
        # Message input field
        self.message_entry = tk.Entry(
            input_controls,
            font=('Arial', 12),
            relief='solid',
            borderwidth=2
        )
        self.message_entry.pack(side='left', fill='x', expand=True, padx=(0, 15))
        self.message_entry.bind('<Return>', lambda e: self.send_message())
        
        # Send button
        self.send_button = tk.Button(
            input_controls,
            text="Send",
            font=('Arial', 12, 'bold'),
            bg='#667eea',
            fg='white',
            relief='flat',
            activebackground='#5a6fd8',
            activeforeground='white',
            padx=20,
            command=self.send_message
        )
        self.send_button.pack(side='right')
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to chat!")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             relief='sunken', anchor='w',
                             bg='#f8f9fa', fg='#6c757d')
        status_bar.pack(fill='x', side='bottom')
        
        # Add welcome message
        self.add_message("Hello! I'm Quest-ai, your intelligent AI assistant powered by DeepSeek AI. How can I help you today?", "assistant")
        
        # Set focus to input field
        self.message_entry.focus()
        
    def add_message(self, message, sender):
        """Add a message to the chat display"""
        self.chat_display.config(state='normal')
        
        if sender == "user":
            self.chat_display.insert(tk.END, "You: ", "user")
        elif sender == "assistant":
            self.chat_display.insert(tk.END, "Quest-ai: ", "assistant")
        else:
            self.chat_display.insert(tk.END, "System: ", "system")
            
        self.chat_display.insert(tk.END, message + "\n\n")
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
        
    def send_message(self):
        """Send user message and get AI response"""
        message = self.message_entry.get().strip()
        if not message:
            return
            
        # Add user message to chat
        self.add_message(message, "user")
        self.message_entry.delete(0, tk.END)
        
        # Disable input while processing
        self.message_entry.config(state='disabled')
        self.send_button.config(state='disabled')
        self.status_var.set("AI is thinking...")
        
        # Send to API in separate thread
        def api_call():
            try:
                response = self.api.send_message(message, self.system_prompt)
                # Schedule UI update in main thread
                self.root.after(0, lambda: self.handle_response(response))
            except Exception as e:
                self.root.after(0, lambda: self.handle_response(f"Error: {str(e)}"))
                
        thread = threading.Thread(target=api_call, daemon=True)
        thread.start()
        
    def handle_response(self, response):
        """Handle AI response and update UI"""
        # Add AI response to chat
        self.add_message(response, "assistant")
        
        # Re-enable input
        self.message_entry.config(state='normal')
        self.send_button.config(state='normal')
        self.message_entry.focus()
        self.status_var.set("Ready to chat!")
        
    def clear_chat(self):
        """Clear the chat history"""
        # Clear API conversation history
        self.api.clear_history()
        
        # Clear chat display
        self.chat_display.config(state='normal')
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state='disabled')
        
        # Add welcome message
        self.add_message("Chat cleared! How can I help you?", "assistant")
        self.status_var.set("Chat cleared - Ready for new conversation!")
        
    def on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit Quest-ai?"):
            self.root.destroy()
            
    def run(self):
        """Start the GUI application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

if __name__ == "__main__":
    # This is for testing purposes
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv('DEEPSEEK_API_KEY', 'sk-test')
    
    app = ChatbotGUI(api_key)
    app.run()
