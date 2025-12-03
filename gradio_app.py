import gradio as gr
import requests
from config import API_HOST, API_PORT, DEFAULT_K,TIMEOUT

API_URL = f"http://{API_HOST}:{API_PORT}/chat"

def chat_with_bot(message):
    """Simple chat function - takes message and returns response"""
    try:
        response = requests.post(
            API_URL,
            json={"query": message, "k": DEFAULT_K},
            timeout=TIMEOUT
        )
        response.raise_for_status()
        data = response.json()
        
        return data["answer"]
    
    except requests.exceptions.RequestException as e:
        return f"❌ Error connecting to API: {str(e)}\n\nPlease make sure the FastAPI server is running on {API_URL}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Simple chat interface
with gr.Blocks() as demo:
    gr.Markdown("# 🤖 AgentForce Infotech Internal Chatbot")
    
    chatbot = gr.Chatbot()
    msg = gr.Textbox(
        label="Your Question",
        placeholder="Ask a question about AgentForce Infotech...",
    )
    clear = gr.Button("Clear")
    
    def respond(message, chat_history):
        bot_message = chat_with_bot(message)
        # Use dictionary format for Gradio
        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": bot_message})
        return "", chat_history
    
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: [], None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
