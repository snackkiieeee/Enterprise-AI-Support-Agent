"""
Enterprise Support AI Agent (Backend)
This script sets up a FastAPI server using LangChain and OpenAI to act as a 
customer support agent. It utilizes memory to handle multi-turn conversations.

To run this:
1. pip install fastapi uvicorn langchain langchain-openai pydantic
2. export OPENAI_API_KEY="your_api_key_here"
3. uvicorn ai_support_agent:app --reload
"""

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate

# Initialize FastAPI App
app = FastAPI(
    title="Enterprise AI Support Agent",
    description="API for an autonomous Tier-1 customer support agent.",
    version="1.0.0"
)

# Setup LangChain components
# We use a Window Memory to remember the last 5 interactions (simulating semantic memory limits)
memory = ConversationBufferWindowMemory(k=5)

# Ensure the user has set their OpenAI API key in the environment
if not os.getenv("OPENAI_API_KEY"):
    print("WARNING: OPENAI_API_KEY environment variable not set. Endpoint will fail.")

# We initialize the LLM lazily in the endpoint, but set up the template here
template = """You are a polite, helpful, and concise Tier-1 Enterprise Customer Support Agent.
Your job is to assist customers with basic troubleshooting, account queries, and billing issues.
If a question is too complex, apologize and say you will escalate it to a human agent.

Current conversation:
{history}
Human: {input}
AI Agent:"""

prompt = PromptTemplate(input_variables=["history", "input"], template=template)

class ChatRequest(BaseModel):
    user_input: str
    session_id: str = "default_session" # In a real app, memory is tied to session_id

class ChatResponse(BaseModel):
    reply: str
    session_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Receives user input and returns the AI's response using conversation memory.
    """
    try:
        # Initialize the LLM (gpt-3.5-turbo is cost-effective for Tier 1 support)
        llm = ChatOpenAI(temperature=0.3, model_name="gpt-3.5-turbo")
        
        # Create the conversation chain
        conversation = ConversationChain(
            llm=llm,
            memory=memory,
            prompt=prompt,
            verbose=False
        )
        
        # Generate response
        ai_response = conversation.predict(input=request.user_input)
        
        return ChatResponse(reply=ai_response, session_id=request.session_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/health")
async def health_check():
    """Simple health check endpoint for Docker/AWS deployments."""
    return {"status": "healthy", "model": "gpt-3.5-turbo"}
