import os
import sys
import logging
from PIL import Image
from flask import Blueprint, Flask, jsonify, request
from backend.ImageToFormat import ImageToFormat

# Configure Logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add the Backend Directory to the System Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class ImageToFormat_Prep:
    def __init__(self) -> None:
        """Initialize the ImageToFormat_Prep class."""
        pass

    def run(self, image: Image) -> str:
        """
        Process the given Image and convert it to Text Format.
        """
        try:
            return ImageToFormat(image).ImageToFormat()
        except Exception as e:
            logging.error('An Error Occurred during Image Processing.', exc_info=True)
            raise e


class ImageToFormat_Prep_API:
    """
    A Flask API class to handle Image Uploading and Format Conversion.
    """

    def __init__(self):
        """Initialize the Flask API and define routes."""
        self.app = Flask(__name__)
        self.ImageToFormat_blueprint = Blueprint('ImageToFormat', __name__)
        self.ImageToFormat_blueprint.add_url_rule('/', 'SERVER_STARTED', self.SERVER_STARTED, methods=['GET'])
        self.ImageToFormat_blueprint.add_url_rule('/UploadedImage', 'UploadedImage', self.UploadedImage, methods=['POST'])
        self.ImageToFormat = ImageToFormat_Prep()

    def SERVER_STARTED(self) -> tuple:
        """
        Handles GET requests and confirms if the Server has Started.
        """
        try:
            return jsonify({'response': 200, 'SERVER STARTED': True}), 200
        except Exception as e:
            logging.error('An Error Occurred while Server Startup.', exc_info=True)
            raise e

    def UploadedImage(self) -> tuple:
        """
        Handles POST requests for uploading an Image and processes it to Extract Text.
        """
        try:
            # Retrieve Image from request and open it using PIL
            image = request.files['file']
            image = Image.open(image)

            # Process the Image to get the Text Format
            text = self.ImageToFormat.run(image)

            return jsonify({'response': text}), 200
        except Exception as e:
            logging.error('An Error Occurred while processing the Uploaded Image.', exc_info=True)
            return jsonify({'Error': str(e)}), 400

    def run(self) -> None:
        """
        Start the Flask Application and run the Server.
        """
        try:
            self.app.register_blueprint(self.ImageToFormat_blueprint)
            self.app.run(debug=True)
        except Exception as e:
            logging.error('An Error Occurred while starting the Flask Application.', exc_info=True)
            raise e


if __name__ == '__main__':

    server = ImageToFormat_Prep_API()
    server.run()