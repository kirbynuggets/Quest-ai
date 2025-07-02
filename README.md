# Quest-ai Chatbot

A modern AI-powered chatbot application using DeepSeek AI, built with Python and Tkinter.

## 🚀 Features

- **Modern GUI**: Clean, intuitive interface built with Tkinter
- **AI-Powered**: Uses DeepSeek AI for intelligent conversations
- **Real-time Chat**: Threaded API calls for smooth user experience
- **Conversation History**: Maintains context across messages
- **Error Handling**: Comprehensive error handling and user feedback
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 📋 Requirements

- Python 3.7+
- Internet connection for AI API calls
- DeepSeek API key (get one at https://platform.deepseek.com/)

## 🛠️ Installation

1. **Clone or download this repository**
2. **Install required packages:**
   ```bash
   pip install requests python-dotenv
   ```
3. **Set up your API key:**
   - Edit the `.env` file and replace `your_api_key_here` with your actual DeepSeek API key
   - Or the application will prompt you for the key when you first run it

## 🎯 Usage

### Run the Application
```bash
python main_tkinter.py
```

### Alternative: Direct GUI Test
```bash
python chatbot_gui_tkinter.py
```

### Test API Connection
```bash
python test_api.py
```

## 📁 Project Structure

```
Quest-ai/
├── main_tkinter.py           # Main application entry point
├── chatbot_gui_tkinter.py    # Tkinter GUI implementation
├── deepseek_api.py          # DeepSeek AI API wrapper
├── test_api.py              # API testing utility
├── .env                     # Environment variables (API key)
├── requirements.txt         # Package dependencies
└── README.md               # This file
```

## 🔧 Configuration

### API Key Setup
1. Get your API key from [DeepSeek Platform](https://platform.deepseek.com/)
2. Add it to the `.env` file:
   ```
   DEEPSEEK_API_KEY=sk-your-actual-api-key-here
   ```

### Customization
- **System Prompt**: Modify the `system_prompt` in `chatbot_gui_tkinter.py`
- **UI Colors**: Change color values in the `setup_ui()` method
- **API Settings**: Adjust parameters in `deepseek_api.py`

## ❗ Troubleshooting

### Common Issues

1. **"Payment Required" Error**
   - Your API key may be out of credits
   - Check your account at https://platform.deepseek.com/
   - Add a payment method if required

2. **"Unauthorized" Error**
   - Your API key may be invalid or expired
   - Verify your API key in the DeepSeek platform

3. **Import Errors**
   - Make sure all required packages are installed: `pip install requests python-dotenv`
   - Ensure you're using Python 3.7+

4. **GUI Won't Start**
   - Make sure you have Tkinter installed (comes with most Python installations)
   - On Linux: `sudo apt-get install python3-tk`

### Error Messages
- **Network Error**: Check your internet connection
- **API Response Error**: The API returned an unexpected response format
- **Timeout Error**: Request took too long, try again

## 🔄 Alternative Versions

### PyQt5 Version (Advanced)
If you prefer PyQt5, you can use:
- `chatbot_gui.py` - PyQt5 GUI implementation
- `main.py` - PyQt5 main entry point

**Note**: PyQt5 requires additional system dependencies and is more complex to set up.

### Tkinter Version (Recommended)
- `chatbot_gui_tkinter.py` - Tkinter GUI implementation (current)
- `main_tkinter.py` - Tkinter main entry point (current)

## 📊 API Usage

The application uses the DeepSeek AI API with the following settings:
- **Model**: `deepseek-chat`
- **Max Tokens**: 2000
- **Temperature**: 0.7
- **Conversation History**: Last 20 messages maintained

## 🛡️ Security

- API keys are stored in `.env` file (not committed to version control)
- All API requests use HTTPS
- No sensitive data is logged or stored permanently

## 📝 License

This project is for educational and personal use. Please respect the DeepSeek AI API terms of service.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

---

**Need Help?** 
- Check the DeepSeek documentation: https://platform.deepseek.com/docs
- Verify your API key status in your DeepSeek account
- Run `python test_api.py` to diagnose API issues
