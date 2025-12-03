# Company Internal Chatbot

A RAG (Retrieval Augmented Generation) based chatbot for internal company documentation using LangChain, ChromaDB, Ollama, FastAPI, and Gradio.


## Overview

This chatbot allows employees to query internal company documentation using natural language. It uses RAG (Retrieval Augmented Generation) to:

1. **Retrieve** relevant document chunks from company documentation
2. **Augment** the LLM prompt with retrieved context
3. **Generate** accurate answers based on the company documents

We are using Ollama which pulls the models local to the system as we can't expose the internal documents to internet by using standard hosted models APIs like OpenAI,Claude,Gemini etc. So we don't require internet for this project.

We are assuming our company name is AgentForce Infotech and we generated some custom documents regarding our company in company-docs folder

## Architecture

### RAG Pipeline Flow

```
User Query
    ↓
Document Loading (company-docs/)
    ↓
Text Splitting (Chunking)
    ↓
Vector Embeddings (Ollama - nomic-embed-text)
    ↓
ChromaDB Storage (Local Vector Database)
    ↓
Similarity Search (Retrieve Top K chunks)
    ↓
LLM Prompt (Context + Query)
    ↓
Response Generation (Ollama - qwen3-vl:8b)
    ↓
Answer to User
```

### Components

1. **Document Loader**: Loads all documents from `company-docs/` folder
2. **Text Splitter**: Splits documents into chunks (600 chars, 120 overlap)
3. **Embedding Model**: Ollama `nomic-embed-text` for creating vector embeddings
4. **Vector Store**: ChromaDB for storing and retrieving embeddings
5. **LLM**: Ollama `qwen3-vl:8b` for generating responses
6. **API**: FastAPI backend for chat endpoint
7. **UI**: Gradio frontend for user interface

## RAG Implementation Details

### Vector Store (ChromaDB)

**ChromaDB** is used as the local vector database to store document embeddings:

- **Storage**: Persisted locally in `./chroma_db` directory
- **Embeddings**: Created using Ollama's `nomic-embed-text` model
- **Retrieval**: Similarity search to find top K relevant chunks
- **Persistence**: Database persists across restarts

### Document Processing

1. **Loading**: All files from `company-docs/` are loaded (supports `.txt`, `.md`, and files without extensions)
2. **Chunking**: Documents are split using `RecursiveCharacterTextSplitter`:
   - Chunk size: 600 characters
   - Overlap: 120 characters (20% overlap for context preservation)
   - Separators: `["\n\n", "\n", " ", ""]` (hierarchical splitting)
3. **Embedding**: Each chunk is converted to a vector embedding
4. **Storage**: Embeddings stored in ChromaDB with metadata (source file path)

### Retrieval Process

When a user asks a question:

1. **Query Embedding**: User query is converted to an embedding
2. **Similarity Search**: ChromaDB finds top K (default: 3) most similar document chunks
3. **Context Formation**: Retrieved chunks are combined into context
4. **Prompt Creation**: Context + query are formatted into a prompt
5. **LLM Generation**: Ollama LLM generates answer based on context

### Response Generation

- **Model**: `qwen3-vl:8b` via Ollama
- **Temperature**: 0.3 (low for factual, consistent answers)
- **Prompt Template**: System message + context + user query
- **Response Cleaning**: Removes reasoning/metadata tags from LLM output

## Project Structure

```
company-internal-chatbot/
├── api.py                 # FastAPI backend with /chat endpoint
├── gradio_app.py          # Gradio frontend UI
├── document_loader.py     # Document loading and vectorstore initialization
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── company-docs/         # Company documentation folder
│   ├── getting-started.txt
│   ├── development-setup
│   ├── ci-cd-pipeline
│   ├── deployment-process.md
│   └── ... (other docs)
└── chroma_db/            # ChromaDB storage (auto-generated, gitignored)
```

## Prerequisites

Before setting up, ensure you have:

1. **Python 3.11+** installed
2. **Ollama** installed and running
   - Download from: https://ollama.com
   - Install required models:
     ```bash
     ollama pull nomic-embed-text
     ollama pull qwen3-vl:8b
     ```

## Setup Instructions

### Step 1: Clone/Download the Project

```bash
cd /path/to/your/projects
# If using git:
# git clone <repository-url>
# cd company-internal-chatbot
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Verify Ollama is Running

```bash
# Check if Ollama is running
ollama list

# If models are not installed, pull them:
ollama pull nomic-embed-text
ollama pull qwen3-vl:8b
```

### Step 5: Add Company Documents

Place your company documentation files in the `company-docs/` folder:

- Supports `.txt`, `.md` files
- Files without extensions are treated as text
- Can have subdirectories (will be loaded recursively)

### Step 6: Initialize Vector Database

The vector database is automatically created when you first run the API:

```bash
# The database will be created automatically on first run
# Or delete existing database to recreate:
rm -rf chroma_db
```

## Running the Application

### Runing Both Services

**Terminal 1 - Start FastAPI Backend:**
```bash
python api.py
# Or
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Start Gradio Frontend:**
```bash
python gradio_app.py
```

### Access Points

- **Gradio UI**: http://localhost:7860
- **FastAPI Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

## Configuration

Edit `config.py` to customize settings:

```python
# Embedding Model
EMBEDDING_MODEL = "nomic-embed-text"

# LLM Model
LLM_MODEL = "qwen3-vl:8b"
LLM_TEMPERATURE = 0.3  # Lower = more factual, Higher = more creative

# Document Settings
DOCUMENTS_FOLDER = "company-docs"
CHROMA_DB_PATH = "./chroma_db"

# Chunking Settings
CHUNK_SIZE = 600        # Size of each chunk
CHUNK_OVERLAP = 120     # Overlap between chunks (20%)

# Retrieval Settings
DEFAULT_K = 3           # Number of documents to retrieve

# Server Settings
API_HOST = "0.0.0.0"
API_PORT = 8000
GRADIO_PORT = 7860
```

## Usage

### Using Gradio UI

1. Start both services (API and Gradio)
2. Open http://localhost:7860 in your browser
3. Type your question in the text box
4. Press Enter or click "Send"
5. View the answer and source documents

### Using API Directly

**Example Request:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the CI/CD pipeline process?",
    "k": 3
  }'
```

**Example Response:**
```json
{
  "answer": "AgentForce Infotech uses GitLab CI/CD...",
  "sources": [
    "company-docs/ci-cd-pipeline",
    "company-docs/deployment-process.md"
  ]
}
```

## API Endpoints

### POST `/chat`

Main chat endpoint for querying the chatbot.

**Request Body:**
```json
{
  "query": "Your question here",
  "k": 3
}
```

**Response:**
```json
{
  "answer": "Generated answer",
  "sources": ["source1", "source2"]
}
```

### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

### GET `/`

API information.

**Response:**
```json
{
  "message": "AgentForce Infotech Chatbot API",
  "status": "running"
}
```

## Recreating the Vector Database

If you update documents or change chunking parameters:

```bash
# Delete existing database
rm -rf chroma_db

# Restart API - it will automatically recreate the database
python api.py
```

## Author

Anubhav Mandarwal ([Anubhav Mandarwal](https://www.linkedin.com/in/anubhav-mandarwal/))