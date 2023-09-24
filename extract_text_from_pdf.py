from pypdf import PdfReader

reader = PdfReader("wijesekera2018.pdf")
number_of_pages = len(reader.pages)
print("Number of pages: ", number_of_pages)

# Iterate over all the pages and append text to the text file
text = ""
for page in reader.pages:
    text += page.extract_text()

# write text to a text file
with open("text_files/wijesekera2018.txt", "w") as text_file:
    text_file.write(text)

