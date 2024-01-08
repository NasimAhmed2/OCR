import fitz
import re

def extract_text_with_layout(pdf_path):
    pdf_document = fitz.open(pdf_path)
    extracted_text = []

    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]

        # Get blocks of text with their coordinates
        blocks = page.get_text("blocks")
        # print(blocks)
        for block in blocks:
            text = block[4]  # Extracted text
            x, y, _, _ = block[:4]  # Coordinates (left, top, width, height)
            extracted_text.append((x, y,text))

    # Sort the extracted text by y-coordinate to maintain the original layout
    sorted_text = sorted(extracted_text, key=lambda item: item[1])
    # print(extracted_text)
    # Add row numbers to the sorted text
    final_text = []
    current_row = 1
    for i, (x, y, text) in enumerate(sorted_text):
        if i > 0 and abs(sorted_text[i-1][1] - y) < 5:  # Check if text is in close proximity on the y-axis
            row_text = f"row{current_row}-{text.strip()}"
            # row_text = f"{text.strip()}"
            final_text.append(row_text)
        else:
            current_row += 1
            row_text = f"row{current_row}-{text.strip()}"
            # row_text = f"{text.strip()}"
            final_text.append(row_text)
    print(final_text)
    return final_text

# Replace 'path/to/your/pdf_file.pdf' with the actual path to your PDF file
pdf_path = 'pdf/train/sample_pdf5.pdf'
sorted_text=extract_text_with_layout(pdf_path)
def has_only_digits(element):
    return all(char.isdigit() or char.isspace() for char in element)
filtered_words = [word for word in sorted_text if "inv" in word.lower()]
digit_words = []

for word in filtered_words:
    row = word.split('-')[0]
    ts = []
    for word in sorted_text:
        if word.startswith(f"{row}-"):
            w = word.split("-", 1)[1]
            if '\n' in w:
                w = w.split("\n", 1)[0] 
                ts.append(w)
            else:
                ts.append(w)
    if any(has_only_digits(elem) for elem in ts):
        digit_words.append(ts) 

# Check if digit_words is empty after the first loop
if not digit_words:
    # Run the loop again for the next row
    digit_words = []
    for word in filtered_words:
        row = str(int(word.split('-')[0][3:]) + 1)  # Increment the row number
        row = 'row'+row
        ts = []
        for word in sorted_text:
            if word.startswith(f"{row}-"):
                w = word.split("-", 1)[1]
                if '\n' in w:
                    w = w.split("\n", 1)[0] 
                    ts.append(w)
                else:
                    ts.append(w)
        if any(has_only_digits(elem) for elem in ts):
            digit_words.append(ts)       
    

def has_only_digits(element):
    return all(char.isdigit() or char.isspace() for char in element)

def extract_invoice_number(lst):    
    for elem in lst:
        if 'Invoice' in elem:
            for char in lst:
                if char.isdigit():
                    break
            return char
        else:
            for char in lst:
                if char.isdigit():
                    break
            return char            
        
    return None


for lst in digit_words:
    invoice_number = extract_invoice_number(lst)
    if invoice_number:
        print(f"The invoice number is: {invoice_number}")        
        
            
    # print(row)
# print(text)
# print(filtered_words)
# print(digit_words)
# print(text)