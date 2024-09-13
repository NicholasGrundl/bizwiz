"""Encode images for use with llm calls"""
import pathlib
import base64
from io import BytesIO

from PIL import Image


def load_image_from_filepath(filepath: str | pathlib.Path) -> Image.Image:
    """Load an image from a filepath"""
    formats = ['JPEG','PNG']
    return Image.open(filepath, formats=formats)
    

def extract_data_from_image(image:Image.Image)->dict:
    """encode image for llm"""
    
    data = {
        "format": image.format,
        "mode": image.mode,
        "size": image.size,
    }
    
    
    
    #encode
    img_format = image.format
    buffered = BytesIO()
    match img_format:
        case 'JPEG':
            img_media_type = 'image/jpeg'
            image.save(buffered, format=img_format)
        case 'PNG':
            img_media_type = 'image/png'
            image.save(buffered, format=img_format)
       
    encoded_img = base64.b64encode(buffered.getvalue()).decode('utf-8')
    data['encoded'] = encoded_img
    data['media_type'] = img_media_type
    return data

