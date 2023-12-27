from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import pytesseract
import numpy as np
import re
import cv2

# Set the path to the Tesseract executable (you need to have Tesseract installed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Open an image file
# image = Image.open('images/image3.jpg')
# image = Image.open('images/image1.png')
# image = Image.open('images/image6.png')
# image = Image.open('images/image4.webp')
# image = Image.open('images/Capture.png')
# image = cv2.imread('images/Capture.png')
image = cv2.imread('images/image6.png')
# image = cv2.imread('images/image5.png')
# image = cv2.imread('images/image4.png')
# image = cv2.imread('images/image3.jpg')
# image = cv2.imread('images/image2.png')
# image = cv2.imread('images/image1.png')

# Convert image to NumPy array
image_array = np.array(image)
# Apply gamma correction
gamma_corrected_image = np.power(image_array / 255.0, 1.5) * 255.0
# Convert NumPy array back to PIL Image
image = Image.fromarray(gamma_corrected_image.astype(np.uint8))
# Apply preprocessing
image = ImageEnhance.Brightness(image).enhance(0.50)  # Experiment with different values
image = image.resize((3 * image.width, 2 * image.height), Image.LANCZOS)
image = image.filter(ImageFilter.SHARPEN)
image = ImageEnhance.Contrast(image).enhance(4.0)

# Use pytesseract to do OCR on the image
custom_config = r'--oem 3 --psm 4 -l eng'
text = pytesseract.image_to_string(image, config=custom_config)

# # Add a space after each line break
# text_with_spaces = re.sub(r'\n', ' \n', text)

# # Define a whitelist of acceptable characters
# whitelist = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789. -"

# # Filter out unwanted characters using a regular expression
# text = re.sub(f"[^ {re.escape(whitelist)}]", "", text_with_spaces)
print(text)
