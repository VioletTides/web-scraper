import requests
import pytesseract
from PIL import Image
from io import BytesIO

def extract_date(url):
    # Download the image from the URL
    image_url = url
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))

    # Perform OCR on the image to extract text
    extracted_text = pytesseract.image_to_string(image)

    print("Extracted Text:", extracted_text)