import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()

def _get_api_key() -> str:

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to a local .env file "
            "or set it as an environment variable before starting the app."
        )
    return api_key



class llm:

    def __init__(self):

        self.api_key = _get_api_key()
    
    def get_llm_llama(self):

        llm = ChatGroq(model="llama-3.3-70b-versatile",api_key=self.api_key)  ### supporting parallel tool calling
        return llm
    
    def get_llm_gpt120b(self):
        llm = ChatGroq(model="openai/gpt-oss-120b",api_key=self.api_key)  ### not supporting parallel tool calling 
        return llm


groq_llm_llama = llm().get_llm_llama()
groq_llm_opnai = llm().get_llm_gpt120b()