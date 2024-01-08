from google.cloud import vision_v1
from google.cloud.vision_v1 import types


# Create a Vision API client
client = vision_v1.ImageAnnotatorClient()

# Load the image file
with open('images/page-1.png', 'rb') as image_file:
    content = image_file.read()

# Create an image object
image = types.Image(content=content)

# Perform OCR on the image
response = client.text_detection(image=image)
texts = response.text_annotations

# Print detected text
for text in texts:
    print(f'Detected text: {text.description}')
