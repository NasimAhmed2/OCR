import os
import pdfplumber
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import fitz

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    print(type(text))
    return text

def train_text_classifier(data, labels):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(data)

    classifier = MultinomialNB()
    classifier.fit(X, labels)

    return vectorizer, classifier

def test_text_classifier(model, pdf_path):
    text = extract_text_with_layout(pdf_path)
    # text = extract_text_from_pdf(pdf_path)
    # print(text)
    X_test = model[0].transform([text])
    # print(X_test)
    prediction = model[1].predict(X_test)
    # print(prediction[0])
    return prediction[0]

def extract_text_with_layout(pdf_path):
    pdf_document = fitz.open(pdf_path)
    extracted_text = []

    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]

        # Get blocks of text with their coordinates
        blocks = page.get_text("blocks")
        
        for block in blocks:
            text = block[4]  # Extracted text
            x, y, _, _ = block[:4]  # Coordinates (left, top, width, height)
            extracted_text.append((x, y, text))

    # Sort the extracted text by y-coordinate to maintain the original layout
    sorted_text = sorted(extracted_text, key=lambda item: item[1])

    # Add row numbers to the sorted text
    final_text = ''
    for i, (x, y, text) in enumerate(sorted_text):
        if i > 0 and abs(sorted_text[i-1][1] - y) < 5:  # Check if text is in close proximity on the y-axis
            row_text = text.strip()
            final_text=final_text+' '+row_text
        else:
            row_text = text.strip()
            final_text=final_text+row_text
    return final_text

def main():
    # Provided labels for training
    labels = {
        'pdf/train\\JAYESH-111.pdf': '9710001201',
        'pdf/train\\sample_pdf.pdf': 'INV-3337',
        'pdf/train\\sample_pdf1.pdf': '00002222',
        'pdf/train\\sample_pdf2.pdf': '00001',
        'pdf/train\\sample_pdf4.pdf': '1111111',
        'pdf/train\\sample_pdf5.pdf': '142563',
        'pdf/train\\sample_pdf8.pdf': '012554422',
        'pdf/train\\sample_pdf9.pdf': '123456',
        'pdf/train\\sample_pdf10.pdf': 'MHS2324000018532',
        'pdf/train\\sample_pdf11.pdf': '303-B5396',
        'pdf/train\\sample_pdf12.pdf': '9710001210',
        'pdf/train\\sample_pdf13.pdf': '9710001200',
        'pdf/train\\sample_pdf14.pdf': '9710001200',
        'pdf/train\\sample_pdf15.pdf': 'INV-3337',
        'pdf/train\\sample_pdf16.pdf': 'EIF/INV/033/22-23'
        # ... and so on
    }

    # Training
    pdf_directory_train = "pdf/train"
    pdf_files_train = [f for f in os.listdir(pdf_directory_train) if f.endswith(".pdf")]

    data = []
    training_labels = []

    for pdf_file in pdf_files_train:
        pdf_path = os.path.join(pdf_directory_train, pdf_file)

        # text = extract_text_with_layout(pdf_path)

        # Use the provided label for training
        label = labels[pdf_path]  # Default to 'Irrelevant' if not in the provided labels
        data.append(pdf_path)
        training_labels.append(label)

    # Train the text classifier
    model = train_text_classifier(data, training_labels)

    # Testing
    pdf_directory_test = "pdf/test"
    pdf_files_test = [f for f in os.listdir(pdf_directory_test) if f.endswith(".pdf")]

    for pdf_file in pdf_files_test:
        pdf_path = os.path.join(pdf_directory_test, pdf_file)
        # text = extract_text_with_layout(pdf_path)
        # data.append(text)
        # Test the classifier on the test set
        predicted_invoice_number = test_text_classifier(model, pdf_path)

        print(f'Predicted Invoice Number for "{pdf_file}": {predicted_invoice_number}')
        #0000001,3215648,4125896

if __name__ == "__main__":
    main()
