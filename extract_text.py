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

#store the extracted text in MongoDB
 
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client['finance_documents']
collection = db['documents']

# Insert the extracted text into MongoDB
document1 = {"title": "consular insurance", "text": text1}
document2 = {"title": "offering memorandum", "text": text2}
collection.insert_one(document1)
collection.insert_one(document2)
