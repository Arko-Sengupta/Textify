import os
import sys
import logging
from PIL import Image
from flask import Blueprint, Flask, jsonify, request

logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.WARNING)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.ImageToFormat import ImageToFormat

class ImageToFormat_Prep:
    
    def __init__(self):
        pass
        
    def run(self, image):
        try:
            return ImageToFormat(image).ImageToFormat()
        except Exception as e:
            logging.error('An Error Occured: ', exc_info=e)
            raise e

class ImageToFormat_Prep_API:

    def __init__(self):
        self.app = Flask(__name__)
        self.ImageToFormat_blueprint = Blueprint('TextToFormat', __name__)
        self.ImageToFormat_blueprint.add_url_rule('/', 'SERVER_STARTED', self.SERVER_STARTED, methods=['GET'])
        self.ImageToFormat_blueprint.add_url_rule('/UploadedImage', 'UploadedImage', self.UploadedImage, methods=['POST'])
        self.ImageToFormat = ImageToFormat_Prep()
        
    def SERVER_STARTED(self):
        try:
            return jsonify({'response': 200, 'SERVER STARTED': True}), 200
        except Exception as e:
            logging.error('An Error Occured: ', exc_info=e)
            raise e

    def UploadedImage(self):
        try:
            image = request.files['file']
            image = Image.open(image)
            
            text = self.ImageToFormat.run(image)
            
            return jsonify({'response': text}), 200
        except Exception as e:
            logging.error('An Error Occurred: ', exc_info=e)
            return jsonify({'Error': str(e)}), 400
        
    def run(self):
        try:
            self.app.register_blueprint(self.ImageToFormat_blueprint)
            self.app.run(debug=True)
        except Exception as e:
            logging.error('An Error Occured: ', exc_info=e)
            raise e
        
if __name__=='__main__':
      
    server = ImageToFormat_Prep_API()
    server.run()