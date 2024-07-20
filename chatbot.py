#extract text from PDF
import pdfplumber

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

#load the pre-trained LLama 2 model and tokenizer

from transformers import LlamaTokenizer, LlamaForCausalLM


tokenizer = LlamaTokenizer.from_pretrained('llama-2-7b')
model = LlamaForCausalLM.from_pretrained('llama-2-7b')


def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors='pt') # Tokenize the input text
    outputs = model.generate(inputs['input_ids'])  # Generate a response
    return tokenizer.decode(outputs[0], skip_special_tokens=True) # Decode the response 


#query MongoDB 

def query_doc(title):
    document = collection.find_one({"title": title})
    if document:
        return document['text']
    else:
        return "Document not found"
    
# Define a function to generate a response from the model

def chatbot(query):
    if "consular insurance" in query.lower():
        doc_content = query_doc("consular insurance")
    elif "offering memorandum" in query.lower():
        doc_content = query_doc("offering memorandum")
    else:
        doc_content = "Document not found"
    if doc_content != "Document not found":
        return generate_response(doc_content + "\n" + query)
    

# Test the chatbot

def test_chatbot():
    queries = [
        "show me an outline of the rsik factors",
        "tell me about the consular insurance",
        "what are the key financials",
        "what is the purpose of the offering memorandum"
        "unknown query"
    ]
    for query in queries:
        print(f"User: {query}")
        response = chatbot(query)
        print(f"Chatbot: {response}")

test_chatbot()
