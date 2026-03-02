# 🤖 Multi-Tool AI Assistant (LangGraph + Groq)

A production-ready AI assistant built using **LangGraph**, **Groq LLM**, and modular microservices architecture.

This system combines deterministic routing, tool orchestration, and a separate RAG service for scalable, cost-efficient AI deployment.

---

## 🚀 Key Features

### 🧮 Deterministic Tools
- Calculator Tool (sandboxed safe evaluation)
- Weather Tool (OpenWeather API integration)
- Date-Time Tool (timezone-aware, real-time)
- Wikipedia Knowledge Tool

### 📚 RAG Microservice (Separate Application)
- LlamaIndex-powered document QA
- Embedding-based semantic search
- Vector indexing
- REST-based service integration

### 🧠 Intelligent Routing
- Rule-based intent detection
- Regex-based classification
- LLM fallback classifier
- Conditional execution with LangGraph

### ⚡ Cost Optimization
- Deterministic routing for math/time queries
- Reduced LLM recursion
- Recursion limits via LangGraph
- Token-efficient model selection (8B / 70B)

### 🛠 Engineering Practices
- Ruff (linting)
- Black (formatting)
- GitHub Actions CI pipeline
- Unused import detection
- Modular microservice architecture

---

### Why LangGraph?
- Deterministic execution
- Controlled recursion
- State management
- Production-safe agent behavior
- Cost-efficient routing

---

## 🧰 Tech Stack

### Core AI
- Python 3.10+
- LangGraph
- LangChain Core
- Groq LLM (Llama-3.1-8B / 70B)

### RAG Service
- LlamaIndex
- HuggingFace Embeddings
- Vector Indexing

### Tools & APIs
- OpenWeather API
- Wikipedia API
- pytz / zoneinfo

### Backend & Infra
- MongoDB (chat logs / memory)
- FastAPI (RAG microservice)
- Streamlit (optional UI)

### Code Quality
- Ruff
- Black
- GitHub Actions CI/CD

---


---

## 🔁 CI/CD Pipeline

Automated GitHub Actions pipeline includes:

- Dependency installation
- Ruff lint checks
- Black formatting validation
- Unused import detection
- Unit testing with pytest

---

## ⚡ Performance & Cost Strategy

- Deterministic routing avoids unnecessary LLM calls
- Math & DateTime handled without LLM
- RAG isolated as microservice
- Configurable recursion limits
- Model size switching (8B vs 70B)

---

## 🧪 Running the Project

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt