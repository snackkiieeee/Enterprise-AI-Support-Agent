Enterprise Customer Support AI Agent 🤖💬

A robust, backend API for an autonomous Tier-1 Customer Support Agent. Built with FastAPI, LangChain, and OpenAI's GPT models, this agent handles routine customer inquiries, manages multi-turn conversation context, and is designed for low-latency enterprise deployment.

🚀 Key Features

Conversational Memory: Utilizes ConversationBufferWindowMemory to retain context over the last $N$ interactions, enabling natural, human-like multi-turn conversations.

Custom Prompt Engineering: Enforces agent behavior guardrails, ensuring responses are polite, concise, and escalated to a human agent when necessary.

High-Performance API: Built on FastAPI, offering asynchronous request handling for thousands of concurrent users.

Cloud-Ready: Includes a /health endpoint for easy integration with Docker, Kubernetes, and AWS CI/CD pipelines.

🛠️ Technology Stack

Framework: FastAPI, Uvicorn

LLM Orchestration: LangChain

Models: OpenAI API (gpt-3.5-turbo for cost-efficiency in Tier-1 support)

Data Validation: Pydantic

⚙️ Installation & Setup

Clone the repository:

git clone [https://github.com/yourusername/Enterprise-AI-Support-Agent.git](https://github.com/yourusername/Enterprise-AI-Support-Agent.git)
cd Enterprise-AI-Support-Agent


Install dependencies:

pip install -r requirements.txt


Set your OpenAI API Key:

# On Linux/macOS
export OPENAI_API_KEY="your-api-key-here"

# On Windows
set OPENAI_API_KEY="your-api-key-here"


Start the FastAPI Server:

uvicorn ai_support_agent:app --reload


📡 API Endpoints

POST /chat

Interact with the AI agent.
Request Body:

{
  "user_input": "I need help resetting my password.",
  "session_id": "user_12345"
}


Response:

{
  "reply": "I can certainly help you with that. Please navigate to the login page and click on 'Forgot Password' to receive a reset link.",
  "session_id": "user_12345"
}


GET /health

Used by load balancers to check service status.

🚢 Deployment (Docker)

This application is designed to be easily containerized.

FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "ai_support_agent:app", "--host", "0.0.0.0", "--port", "8000"]
