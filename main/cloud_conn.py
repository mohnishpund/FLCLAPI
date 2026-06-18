import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Establish the "Connection" to Cloudinary
cloudinary.config(
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key = os.getenv('CLOUDINARY_API_KEY'),
    api_secret = os.getenv('CLOUDINARY_API_SECRET'),
    secure = True
)

def upload_image_to_cloud(file_obj, filename, content_type):
    """
    Uploads an image file to Cloudinary.
    """
    try:
        # Cloudinary can accept the file object directly
        response = cloudinary.uploader.upload(
            file_obj,
            public_id = filename.rsplit('.', 1)[0], # Removes extension from name
            folder = "flask_uploads"                 # Optional: organizes images into a folder
        )
        
        # Cloudinary automatically returns the secure hosting URL
        return response.get('secure_url')
        
    except Exception as e:
        return f"Error: {str(e)}"