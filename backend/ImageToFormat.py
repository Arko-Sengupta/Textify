import os
import sys
import easyocr
import logging
import numpy as np
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Reconfigure the Stdout to Handle UTF-8 Encoding
sys.stdout.reconfigure(encoding='utf-8')

# Configure Logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Load Environment Variables
load_dotenv(".env.local")


class ImageToFormat:
    def __init__(self, Image: np.array) -> None:
        """Initialize the ImageToFormat class by setting the image and loading the API Key."""
        self.Image = Image
        self.API_KEY = os.getenv("API_KEY")
        if not self.API_KEY:
            raise ValueError("API_KEY not found in Environment Variables.")
        self.model = ChatOpenAI(openai_api_key=self.API_KEY)

    def Prompt(self) -> PromptTemplate:
        """
        Creates a prompt template for formatting and correcting the extracted text.
        """
        try:
            return PromptTemplate.from_template("Please format and correct the content without adding extra information: {content}.")
        except Exception as e:
            logging.error("An Error Occurred while Generating the Prompt Template.", exc_info=True)
            raise e

    def LLMChain(self) -> LLMChain:
        """
        Initializes an LLMChain with the OpenAI Model and Prompt.
        """
        try:
            return LLMChain(llm=self.model, prompt=self.Prompt())
        except Exception as e:
            logging.error("An error occurred while initializing the LLMChain.", exc_info=True)
            raise e

    def OpenAI(self, text: str) -> str:
        """
        Sends the Extracted Text to OpenAI for Formatting and Grammatical Correction.
        """
        try:
            chain = self.LLMChain()
            return chain.run(content=text)
        except Exception as e:
            logging.error("An Error Occurred during the OpenAI API Call.", exc_info=True)
            raise e

    def ImageToFormat(self, lang: str = 'en') -> str:
        """
        Processes the Image and then sends the Extracted Text for Formatting.
        """
        try:
            # Read Text from Image
            reader = easyocr.Reader([lang])
            text_data = reader.readtext(np.array(self.Image))

            # Extract the Text from the OCR
            text = " ".join([t for _, t, _ in text_data])

            # Format the Text using OpenAI's API
            formatted_text = self.OpenAI(text)
            return formatted_text
        except Exception as e:
            logging.error("An Error Occurred during the Image processing or Text Formatting.", exc_info=True)
            raise e