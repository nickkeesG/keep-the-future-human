import os
from anthropic import Anthropic
import yaml
from dotenv import load_dotenv

load_dotenv()


class AnthropicClient:
    def __init__(self, config_path: str = "config/settings.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.client = Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )
        self.model = self.config['api']['model']
    
    def send_message(self, message: str, system_prompt: str = None) -> str:
        """Send a message to Claude and return the response"""
        try:
            kwargs = {
                "model": self.model,
                "messages": [{"role": "user", "content": message}],
                "max_tokens": 16384  # Good balance for translations
            }
            if system_prompt:
                kwargs["system"] = system_prompt
            
            response = self.client.messages.create(**kwargs)
            return response.content[0].text
        except Exception as e:
            raise Exception(f"API call failed: {str(e)}")