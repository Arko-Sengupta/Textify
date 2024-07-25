import os
import logging
import requests
import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_JUSTIFY
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.WARNING)

load_dotenv(".env")

class Textify_UI:
    
    def __init__(self) -> None:
        self.AppName = os.getenv("AppName")
        self.AppImgUpload = os.getenv("AppImgUpload")
        self.AppImgUploded = os.getenv("AppImgUploaded")
        self.Buffer = BytesIO()
        self.ImageToFormat_API = os.getenv("ImageToFormat_API")
        
    def ConvertToPDF(self, text):
        try:
            pdf = SimpleDocTemplate(self.Buffer, pagesize=letter, title="Document")
            
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name='Justified', alignment=TA_JUSTIFY, fontName='Times-Roman', fontSize=12, leading=24))
            
            paragraphs = text.split('\n\n')
            flowables = []
            
            for para in paragraphs:
                flowables.append(Paragraph(para, styles['Justified']))
                flowables.append(Spacer(1, 12))
                
            pdf.build(flowables)
            self.Buffer.seek(0)
            return self.Buffer.getvalue()   
        except Exception as e:
            logging.error("An Error Occurred: ", exc_info=e)
            raise e
    
    def AppHeader(self):
        try:
            st.title(self.AppName)
        except Exception as e:
            logging.error("An Error Occured: ", exc_info=e)
            raise e
        
    def AppSubHeader(self, subtitle):
        try:
            st.subheader(subtitle)
        except Exception as e:
            logging.error("An Error Occured: ", exc_info=e)
            raise e
        
    def run(self):
        try:
            self.AppHeader()
                   
            self.AppSubHeader(self.AppImgUpload)
            uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
            
            if uploaded_file is not None:
                
                self.AppSubHeader(self.AppImgUploded)
                st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                upload_button = st.button("Upload Image")
                
                if upload_button:
                   with st.spinner("Generating PDF"):
                       response = requests.post(self.ImageToFormat_API, files=files)
    
                       if response.status_code == 200:
                          pdf_buffer = self.ConvertToPDF(response.json()['response'])
                          st.download_button(
                              label="Download PDF",
                              data=pdf_buffer,
                              file_name="Document.pdf",
                              mime="application/pdf",
                          )
                       else:
                           st.error(f"Failed to upload image. Status code: {response.status_code}")
                           st.text(response.text)
            
        except Exception as e:
            logging.error("An Error Occured: ", exc_info=e)
            raise e

if __name__=='__main__':
    
    App = Textify_UI()
    App.run()