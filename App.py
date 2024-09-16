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

# Configure Logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Load Environment Variables
load_dotenv(".env")

class Textify_UI:
    def __init__(self) -> None:
        """Initialize the Textify_UI class by loading Environment Variables."""
        self.AppName = os.getenv("AppName")
        self.AppImgUpload = os.getenv("AppImgUpload")
        self.AppImgUploaded = os.getenv("AppImgUploaded")
        self.Buffer = BytesIO()
        self.ImageToFormat_API = os.getenv("ImageToFormat_API")
        
    def ConvertToPDF(self, text: str) -> bytes:
        """
        Converts the provided text into a PDF document.
        """
        try:
            # Create PDF Document in Memory
            pdf = SimpleDocTemplate(self.Buffer, pagesize=letter, title="Document")
            
            # Define Styles for the Document
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name='Justified', alignment=TA_JUSTIFY, fontName='Times-Roman', fontSize=12, leading=24))
            
            # Split Text into Paragraphs and add to Flowable Objects
            paragraphs = text.split('\n\n')
            flowables = []
            
            for para in paragraphs:
                flowables.append(Paragraph(para, styles['Justified']))
                flowables.append(Spacer(1, 12))
                
            # Build the PDF Document
            pdf.build(flowables)
            self.Buffer.seek(0)
            return self.Buffer.getvalue()   
        except Exception as e:
            logging.error("An Error Occurred during PDF Generation.", exc_info=True)
            raise e
    
    def AppHeader(self) -> None:
        """
        Define Main Header.
        """
        try:
            st.title(self.AppName)
        except Exception as e:
            logging.error("An Error Occurred while setting the App Header.", exc_info=True)
            raise e
        
    def AppSubHeader(self, subtitle: str) -> None:
        """
        Define Subheader.
        """
        try:
            st.subheader(subtitle)
        except Exception as e:
            logging.error("An Error Occurred while setting the App Subheader.", exc_info=True)
            raise e
        
    def run(self) -> None:
        """
        Runs the Main Application Logic, Handling Image Uploads and PDF Generation.
        """
        try:
            # Display the Main Header and Image Upload Prompt
            self.AppHeader()    
            self.AppSubHeader(self.AppImgUpload)

            uploaded_file = st.file_uploader("Choose an Image...", type=["jpg", "jpeg", "png"])
            
            if uploaded_file is not None:
                # Uploaded Image and Prompt
                self.AppSubHeader(self.AppImgUploaded)
                st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            
                # Prepare file for Upload
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                upload_button = st.button("Upload Image")
                
                if upload_button:
                    with st.spinner("Generating PDF..."):
                        response = requests.post(self.ImageToFormat_API, files=files)
    
                        if response.status_code == 200:
                            # Convert Response Text to PDF
                            pdf_buffer = self.ConvertToPDF(response.json()['response'])
                            st.download_button(
                                label="Download PDF",
                                data=pdf_buffer,
                                file_name="Document.pdf",
                                mime="application/pdf",
                            )
                        else:
                            st.error(f"Failed to Upload Image. Status Code: {response.status_code}")
                            st.text(response.text)
        except Exception:
            logging.error("An Error Occurred while running the App.", exc_info=True)
            st.error("Failed to Upload Image. Please try Again!")

if __name__ == '__main__':

    App = Textify_UI()
    App.run()
