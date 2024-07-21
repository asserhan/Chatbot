# Chatbot

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/asserhan/Chatbot.git
   cd https://github.com/asserhan/Chatbot.git

2. **set up env**

    ```bash
    python3 -m venv chatbot-env
    source chatbot-env/bin/activate

3. **install dependencies**
    ```bash
    pip install -r requirements.txt

4. **Verify Installation**

    ```bash
    python -c "import torch; print('PyTorch version:', torch.__version__)"
    python -c "import transformers; print('Transformers version:', transformers.__version__)"
    python -c "import pymongo; print('PyMongo version:', pymongo.__version__)"
    python -c "import langchain; print('LangChain version:', langchain.__version__)"
    python -c "import pdfplumber; print('pdfplumber version:', pdfplumber.__version__)"


5. **MongoDB Setup**

    You need to have MongoDB server running on your local machine. Follow these steps to install and start MongoDB:

    ```bash
    brew tap mongodb/brew
    brew install mongodb-community
    brew services start mongodb-community


