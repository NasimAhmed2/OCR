import cv2
import pytesseract

# Path to the Tesseract OCR executable (update it based on your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Read the image using OpenCV
# image = cv2.imread('images/image1.png')
# image = cv2.imread('images/image2.png')
# image = cv2.imread('images/image3.jpg')
# image = cv2.imread('images/image4.png')
# image = cv2.imread('images/image5.png')
image = cv2.imread('images/image6.png')
# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Use OpenCV to perform image preprocessing (e.g., thresholding, denoising)
# Here, we use a simple thresholding example
_, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)

# Convert the OpenCV binary image to a PIL Image
from PIL import Image
pil_image = Image.fromarray(binary_image)
# Use pytesseract to do OCR on the image
custom_config = r'--oem 3 --psm 4 -l eng'
# Use pytesseract to perform OCR on the preprocessed image
text = pytesseract.image_to_string(pil_image, config=custom_config, lang='eng')

print(text)
