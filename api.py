from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from document_loader import vectorstore
from config import *
import re

app = FastAPI(
    title="AgentForce Infotech Chatbot API",
    description="Internal documentation chatbot API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = ChatOllama(
    model=LLM_MODEL,
    temperature=LLM_TEMPERATURE
)

def clean_response(text):
    if not text:
        return text
    
    reasoning_patterns = [
        r'`</think>`',
        r'`</think>`',
        r'</think>',
        r'</think>',
        r'</text>',
        r'</thinking>',
        r'</reasoning>',
    ]
    
    last_match = None
    last_pos = -1
    
    for pattern in reasoning_patterns:
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        if matches:
            match = matches[-1]
            if match.end() > last_pos:
                last_pos = match.end()
                last_match = match
    
    if last_match:
        return text[last_match.end():].strip()
    
    lines = text.split('\n')
    cleaned_lines = []
    found_answer = False
    
    for i, line in enumerate(lines):
        if re.match(r'^[-*]\s*(I should|I\'ll|I can|Let me)', line, re.IGNORECASE):
            continue
        if not found_answer and line.strip() and not re.match(r'^[-*]', line):
            found_answer = True
        if found_answer:
            cleaned_lines.append(line)
    
    result = '\n'.join(cleaned_lines).strip()
    
    return result if result else text.strip()

prompt_template = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant for AgentForce Infotech. 
Answer questions based ONLY on the provided context from company documents.

IMPORTANT RULES:
- Provide direct answers only
- Do NOT include any thinking, reasoning tags, or metadata
- Do NOT say things like "I'll organize" or include tags like `</think>`
- Do NOT include any reasoning process
- Answer concisely and professionally"""),
    
    ("user", """Context from company documents:
{context}

Question: {query}

Answer:""")
])

output_parser = StrOutputParser()

qa_chain = prompt_template | llm | output_parser

class ChatRequest(BaseModel):
    query: str
    k: int = DEFAULT_K

class ChatResponse(BaseModel):
    answer: str
    sources: list[str]

@app.get("/")
def root():
    return {"message": "AgentForce Infotech Chatbot API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        retrieved_docs = vectorstore.similarity_search(request.query, k=request.k)
        
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        sources = [doc.metadata.get('source', 'unknown') for doc in retrieved_docs]
        
        answer = qa_chain.invoke({
            "context": context,
            "query": request.query
        })
        
        answer = clean_response(answer)
        
        return ChatResponse(
            answer=answer, 
            sources=sources
        )
    
    except Exception as e:
        return ChatResponse(
            answer=f"Error: {str(e)}",
            sources=[]
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)
