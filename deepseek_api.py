import requests
import json
from typing import Dict, List, Optional

class DeepSeekAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        self.conversation_history = []
    
    def send_message(self, message: str, system_prompt: str = None) -> Optional[str]:
        """Send a message to DeepSeek AI and get response"""
        try:
            # Build messages array
            messages = []
            
            # Add system prompt if provided
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            # Add conversation history
            messages.extend(self.conversation_history)
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": message
            })
            
            # Prepare the request payload
            payload = {
                "model": "deepseek-chat",
                "messages": messages,
                "max_tokens": 2000,
                "temperature": 0.7,
                "stream": False
            }
            
            # Make the API request
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            
            # Parse response
            result = response.json()
            assistant_message = result['choices'][0]['message']['content']
            
            # Update conversation history
            self.conversation_history.append({
                "role": "user",
                "content": message
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            # Keep conversation history manageable (last 10 exchanges)
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return assistant_message
            
        except requests.exceptions.RequestException as e:
            return f"Network error: {str(e)}"
        except KeyError as e:
            return f"API response error: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_conversation_history(self) -> List[Dict]:
        """Get current conversation history"""
        return self.conversation_history.copy()