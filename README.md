# Chatbot

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. **set up env**
    python3 -m venv chatbot-env
    source chatbot-env/bin/activate

3. **install dependencies**
    pip install -r requirements.txt

4. **Verify Installation**

    python -c "import torch; print('PyTorch version:', torch.__version__)"
    python -c "import transformers; print('Transformers version:', transformers.__version__)"
    python -c "import pymongo; print('PyMongo version:', pymongo.__version__)"
    python -c "import langchain; print('LangChain version:', langchain.__version__)"
    python -c "import fitz; print('PyMuPDF version:', fitz.__doc__)"
