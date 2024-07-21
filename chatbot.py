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
import certifi

# Connect to MongoDB
mongo_uri = "mongodb://localhost:27017/"
try:
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    # Attempt to fetch server information to ensure connectivity
    client.server_info()
    print("MongoDB connection successful!")
except Exception as e:
    print(f"MongoDB connection error: {e}")
db = client['finance_documents']
collection = db['documents']

# Insert the extracted text into MongoDB
document1 = {"title": "consular insurance", "text": text1}
document2 = {"title": "offering memorandum", "text": text2}
collection.insert_one(document1)
collection.insert_one(document2)

#load the pre-trained model

from transformers import GPT2LMHeadModel, GPT2Tokenizer

model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Add padding token to tokenizer
tokenizer.pad_token = tokenizer.eos_token

def generate_response(prompt):
    inputs = tokenizer.encode(prompt, return_tensors='pt', max_length=512, truncation=True)
    attention_mask = inputs.ne(tokenizer.pad_token_id).float()
    outputs = model.generate(
        inputs,
        attention_mask=attention_mask,
        max_length=150,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        temperature=0.7
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


#query MongoDB 

def query_doc(title):
    try:
        document = collection.find_one({"title": title})
        if document:
            return document['text']
        else:
            return "Document not found"
    except Exception as e:
        print(f"Error querying database: {e}")
        return "Error accessing document"

def chatbot(query):
    doc_content = ""
    if "consular insurance" in query.lower():
        doc_content = query_doc("consular insurance")
    elif "offering memorandum" in query.lower():
        doc_content = query_doc("offering memorandum")
    
    if doc_content and doc_content != "Document not found":
        # Truncate document content
        max_doc_length = 300  # Adjust based on your needs
        truncated_doc = doc_content[:max_doc_length]
        
        prompt = f"Document excerpt: {truncated_doc}\n\nQuestion: {query}\n\nAnswer:"
        response = generate_response(prompt)
        
        # Post-process to ensure relevance
        if query.lower() in response.lower() or any(keyword in response.lower() for keyword in query.lower().split()):
            return response
        else:
            return "I'm sorry, I couldn't find a relevant answer to your question in the document."
    else:
        return "I'm sorry, I couldn't find the document you're referring to or there was an error accessing it."

def test_chatbot():
    queries = [
        "Show me an outline of the risk factors in the offering memorandum",
        "Tell me about the consular insurance",
        "What are the key financials mentioned in the offering memorandum?",
        "What is the purpose of the offering memorandum?",
        "Unknown query"
    ]
    for query in queries:
        print(f"User: {query}")
        response = chatbot(query)
        print(f"Chatbot: {response}\n")

test_chatbot()
