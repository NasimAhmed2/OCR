import fitz
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import pytesseract
import numpy as np
import re
import cv2
from pytesseract import Output

def extract_text_with_layout(pdf_path):
    pdf_document = fitz.open(pdf_path)
    extracted_text = []

    # Process only the first page
    page_num = 0
    page = pdf_document[page_num]

    # Get text-based blocks
    text_blocks = [block for block in page.get_text("blocks") if block[5] == 0]
    print(text_blocks)
    for block in text_blocks:
        text = block[4]  # Extracted text
        x, y, _, _ = block[:4]  # Coordinates (left, top, width, height)
        extracted_text.append(text)

    # Get image-based blocks
    image_blocks = [block for block in page.get_images(full=True)]
    print(image_blocks)
    for image_block in image_blocks:
        # Extract image data
        image_data = image_block[0]
        print('hello')
        # Convert image data to NumPy array
        image_array = np.array(image_data)
        # Convert image to NumPy array
        # image_array = np.array(image_data)

        # Convert NumPy array back to PIL Image
        processed_image = Image.fromarray(image_array.astype(np.uint8))

        # Use pytesseract to do OCR on the processed image
        custom_config = r'--oem 3 --psm 12 -l eng'
        text = pytesseract.image_to_string(processed_image, config=custom_config)
        print(f"Image block: {image_block[4]}")
        print(f"OCR Text: {text}")

    print(extracted_text)

# Replace 'path/to/your/pdf_file.pdf' with the actual path to your PDF file
pdf_path = 'pdf/train/sample_pdf10.pdf'
extract_text_with_layout(pdf_path)
