import sys
import easyocr
import logging

sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.WARNING)

class ImageToText:
    
    def __init__(self, ImagePath):
        self.ImagePath = ImagePath
        
    def ImageToText(self, lang='en'):
        try:
            text = easyocr.Reader([lang]).readtext(self.ImagePath)
            text = " ".join([t for _, t, _ in text])
            
            return text
        except Exception as e:
            logging.error('An Error Occured: ', exc_info=e)
            raise e

if __name__ == "__main__":
    
    ImagePath = 'Demo Image 1.png'
    text = ImageToText(ImagePath).ImageToText()
    print(text)