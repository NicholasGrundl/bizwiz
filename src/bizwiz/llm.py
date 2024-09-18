"""Manage LLM clients and keys"""
import os
import pathlib
from typing import Any

from dotenv import load_dotenv
import anthropic

from .image import load_image_from_filepath, extract_data_from_image

def load_llm_env(llm_vendors: list[str] | None = None) -> bool:
    """Load the env and check for LLM environment variables"""
    load_dotenv()
    required_env_vars = [
        'OPENAI_API_KEY',
        'ANTHROPIC_API_KEY',
    ]
    
    for env_var in required_env_vars:
        if env_var not in os.environ:
            #missing a key
            raise KeyError(f"Missing required environment variable: {env_var}")
    return True
    

DEFAULT_MODELS = {
    'openai' : '',
    'anthropic' : 'claude-3-haiku-20240307',
}

DEFAULT_MAX_TOKENS = {
    'openai' : None,
    'anthropic' : 4096,
}

class ChatManager:
    """Manage the main aspects of a chat in a more structured way"""

    def __init__(
        self,
        temperature : float = 0.0,
    ):  
        #load env vars
        load_llm_env()


        #model level attributes
        self.client = anthropic.Client()
        self.model = 'claude-3-5-sonnet-20240620'
        self.temperature = temperature
        self.max_tokens = 4096

        #agent level attributes
        self.system_prompt = ''
        self.conversation = []
        
    ## methods
    # -- actions     
    def prompt(
        self, 
        text : str,
        image_filepath : str | pathlib.Path | None = None,
    )-> str:
        """Prompt the model with a message and return the answer
        - updates the history
        """
        messages = [message for message in self.conversation]
        message = self.get_message(text=text, image_filepath=image_filepath)
        
        messages.append(message)

        client = self.client
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=self.system_prompt,
            messages=messages,
            temperature=self.temperature,
        )

        #handle response
        # TODO: add error handling
        answer = response.content[-1].text

        #update conversation
        self.conversation.append(message)
        self.conversation.append({'role' : 'assistant', 'content' : answer})
        return answer

    def clear_conversation(self)->None:
        """Clear the conversation"""
        self.conversation = []
        return True
    
    def undo_last_message(self, n:int=1)->None:
        """Remove the last message from the conversation
        
        n: rounds to undo, defaults to 1
            - a round is a user + assistant message
        """
        if n*2 > len(self.conversation):
            self.clear_conversation()
            return True
        
        n_messages = len(self.conversation)
        n_end = n_messages - 2*n #user and assistant
        new_messages = []
        for i, message in enumerate(self.conversation):
            if i>=n_end:
                break
            new_messages.append(message)
        self.conversation = new_messages
        return True
        


    

    # -- utility
    def set_system_prompt(self, prompt: str) -> None:
        """Set the system prompt specific to the client"""
        self.system_prompt = prompt


    def get_message(self, text: str, image_filepath : str | pathlib.Path | None = None)->list[dict[str,Any]]:
        """Return a message object
        
        - allow text
        - allow image via path
        """
        content = []
        text_content = self.get_text_content(text)
       
        if image_filepath is not None:
             #add image to content if present
            image_content = self.get_image_content(image_filepath)
            if image_content is not None:
                content.append(image_content)

        content.append(text_content)
        return {'role' : 'user' , 'content' : content}

    def get_text_content(self, text :str)->dict[str,str]:
        """Return a text message object"""
        return {
            "type": "text",
            "text": text,
        }
    
    def get_image_content(self, filepath: str | pathlib.Path)->dict[str,Any] | None:
        """Return an image message object"""
        #load image
        image_data = load_image_from_filepath(filepath)
        if image_data is None:
            return None
        #encode image
        encoded_image_data = extract_data_from_image(image_data)
        
        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": encoded_image_data['media_type'],
                "data": encoded_image_data['encoded'],
            },
        }