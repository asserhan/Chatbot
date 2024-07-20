import pdfplumber

#extract text from PDF

def extract(pdf_path):
    text=""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text+=page.extract_text() + "\n"
    return text

#extract text from both documents
text1 = extract("Data/consular insurance.pdf")
text2 = extract("Data/offering memorandum.pdf")

print("Extracted text from offering_memorandum.pdf:\n")
print(text1)
