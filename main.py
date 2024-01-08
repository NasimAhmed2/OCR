from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import pytesseract
import numpy as np
import re
import cv2
from pytesseract import Output

# Set the path to the Tesseract executable (you need to have Tesseract installed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Open an image file
# image = Image.open('images/image3.jpg')
# image = Image.open('images/image1.png')
# image = Image.open('images/image6.png')
# image = Image.open('images/image4.webp')
# image = Image.open('images/Capture.png')
# image = cv2.imread('images/Capture.png')
image = cv2.imread('images/page-1.png')
# image = cv2.imread('images/image6.png')
# image = cv2.imread('images/image5.png')
# image = cv2.imread('images/image4.png')
# image = cv2.imread('images/image7.jpg')
# image = cv2.imread('images/image2.png')
# image = cv2.imread('images/image1.png')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# Convert image to NumPy array
image_array = np.array(image)
shape = image.shape
# Apply gamma correction
gamma_corrected_image = np.power(image_array / 255.0, 1.5) * 255.0
# Set the parameters for the UnsharpMask filter
radius = 3
percent = 100
threshold = 3
# Convert NumPy array back to PIL Image
image = Image.fromarray(gamma_corrected_image.astype(np.uint8))
# # Apply preprocessing images/page-2.png
# image = ImageEnhance.Brightness(image).enhance(0.60)  # Experiment with different values
# image = image.resize((3 * image.width, 2 * image.height), Image.LANCZOS)
# # image = image.filter(ImageFilter.SHARPEN)
# image = image.filter(ImageFilter.UnsharpMask(radius=radius, percent=percent, threshold=threshold))
# image = ImageEnhance.Contrast(image).enhance(1)

# Apply preprocessing images/page-1.png
image = ImageEnhance.Brightness(image).enhance(1.0)  # Experiment with different values
image = image.resize((3 * image.width, 2 * image.height), Image.LANCZOS)
# image = image.filter(ImageFilter.SHARPEN)
image = image.filter(ImageFilter.UnsharpMask(radius=radius, percent=percent, threshold=threshold))
image = ImageEnhance.Contrast(image).enhance(1)

# Use pytesseract to do OCR on the image
custom_config = r'--oem 3 --psm 4 -l eng'
text = pytesseract.image_to_string(image, config=custom_config)
lines = text.split('\n')
numbered_lines = [f"row{i + 1}:{line}" for i, line in enumerate(lines)]
print(text)
def meets_conditions(word):
    if word.isdigit() or word.isalpha():
        pass
    else:
        conditions = [
            word[:2].isdigit(),  # Condition 1
            word[2:7].isalpha(),  # Condition 2
            word[7:11].isdigit(),  # Condition 3
            word[11].isalpha(),  # Condition 4
            word[12].isdigit(),  # Condition 5
            word[13:].isalpha(),  # Condition 6
            
        ]
        return sum(conditions) >= 3
def extract_invoice_number(xt):
    # Define a regular expression pattern for extracting invoice numbers
    # pattern = re.compile(r'(?i)(Inv\.?|Invoice|Inv. No.|PL NO.|Invoice No)\D*(\d+)')
    Invoice_pattern = re.compile(r'(?i)(Inv\.?|Invoice|Inv. No.|PL NO.|Invoice No)\D*(?=(\d{3,}))')
    Bill_pattern = re.compile(r'(?i)(Bill\.?|Bill|Bill. No.|Bill NO.|B/L NO.|Bill No)\D*(?=(\d{3,}))')
    # Date_pattern = re.compile(r'\b(\d{2}[/.-]\d{2}[/.-]\d{4})\b')
    Date_pattern = re.compile(r'\b(\d{2}[/.-]\d{2}[/.-]\d{2,4}|\d{2}-[a-zA-Z]+-\d{2,4})\b')
    Amount_pattern = re.compile(r'(?i)(Inv\.?|Invoice|Inv. No.|PL NO.|Invoice No)\D*(?=(\d{3,}))')
    

    # Extract words of length 15
    words = re.findall(r'\b\w{15}\b', xt)
    # Filter words that meet at least two conditions
    GST = [word for word in words if meets_conditions(word)]
    # Search for matches in the text
    Invoice = Invoice_pattern.findall(xt)
    print(Invoice)
    Bill = Bill_pattern.findall(xt)
    Date = Date_pattern.findall(xt)
    # GST = GST_pattern.findall(xt)
    # print(xt)
    # Extract the numeric part from each match
    # invoice_numbers = [match[1] for match in matches]
    invoice_numbers = [match[1] for match in Invoice if len(match[1]) > 2]
    Bill_numbers = [match[1] for match in Bill]
    
    print("The Invoice Number is:",invoice_numbers)
    print("The Bill Number is:",Bill_numbers)
    print("The GST Number is:",GST)
    print("Bill Date",Date)
extract_invoice_number(text)
# print(numbered_lines)
# # Add a space after each line break
# text_with_spaces = re.sub(r'\n', ' \n', text)

# # Define a whitelist of acceptable characters
# whitelist = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789. -"

# # Filter out unwanted characters using a regular expression
# text = re.sub(f"[^ {re.escape(whitelist)}]", "", text_with_spaces)



