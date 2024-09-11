"""Manage LLM clients and keys"""
import os

from dotenv import load_dotenv
import anthropic

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
        
    #methods    
    def set_system_prompt(self, prompt: str) -> None:
        """Set the system prompt specific to the client"""
        self.system_prompt = prompt
    
    def promt(self, prompt : str)-> str:
        """Prompt the model with a message and return the answer
        - updates the history
        """
        messages = [message for message in self.conversation]
        message = {'role' : 'user' , 'content' : prompt}
        
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
        self.conversation.append({'role' : 'user', 'content' : prompt})
        self.conversation.append({'role' : 'assistant', 'content' : answer})
        return answer
    

