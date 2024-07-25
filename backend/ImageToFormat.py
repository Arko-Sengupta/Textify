import os
import sys
import easyocr
import logging
import numpy as np
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.WARNING)

load_dotenv(".env.local")

class ImageToFormat:
    
    def __init__(self, Image):
        self.Image = Image
        self.API_KEY = os.getenv("API_KEY")
        self.model = ChatOpenAI(openai_api_key=self.API_KEY)
        
    def Prompt(self):
        try:
            return (PromptTemplate.from_template("Please format and make the content gramatically correct without any addition content: {content}."))
        except Exception as e:
            logging.error("An Error Occured: ", exc_info=e)
            raise e
        
    def LLMChain(self):
        try:
            return LLMChain(llm=self.model, prompt=self.Prompt())
        except Exception as e:
            logging.error('An Error Occured: ', exc_info=e)
            raise e
        
    def OpenAI(self, text):
        try:
           self.chain = self.LLMChain()
           return self.chain.run(content=text)
        except Exception as e:
            logging.error("An Error Occured: ", exc_info=e)
            raise e
        
    def ImageToFormat(self, lang='en'):
        try:
            text = easyocr.Reader([lang]).readtext(np.array(self.Image))
            text = " ".join([t for _, t, _ in text])
            
            text = self.OpenAI(text)
            return text
        except Exception as e:
            logging.error('An Error Occured: ', exc_info=e)
            raise e