
import fitz

# Create a document object
doc = fitz.open('pdf/train/sample_pdf16.pdf')  # or fitz.Document(filename)


page_number = 0
# Get the page by their index
page = doc.load_page(page_number)
 # or page = doc[0]
# Create a new document
new_doc = fitz.open()

# Add the page to the new document
new_doc.insert_pdf(doc, from_page=page_number, to_page=page_number)

# Save the new document as a PDF
new_doc.save('pdf/output_pdf16_page1.pdf')
# read a Page
text = page.get_text()
print(text)

# Render and save the page as an image
pix = page.get_pixmap() 
pix.save(f"page-{page.number}.png")

# # get all links on a page
# links = page.get_links()
# print(links)

# # Render and save all the pages as images

# page = doc.load_page(0)
# pix = page.get_pixmap()
# pix.save("images/page-4.png")

# # get the links on all pages
# for i in range(doc.page_count):
#   page = doc.load_page(i)
#   link = page.get_links()
#   print(link)




