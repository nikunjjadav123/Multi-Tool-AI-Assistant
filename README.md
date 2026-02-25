# 🤖 Multi-Tool AI Assistant (LangGraph + Groq)

A production-ready AI assistant built using **LangGraph**, **Groq LLM**, and multiple deterministic tools.

This system combines rule-based routing with LLM-powered reasoning to create a fast, cost-efficient, and scalable AI agent.

---

## 🚀 Features

- 🧮 Calculator Tool (safe sandboxed evaluation)
- 🌤 Weather Tool (OpenWeather API integration)
- 📚 Wikipedia Tool (knowledge retrieval)
- 🕒 Date-Time Tool (timezone-aware, real-time)
- 🧠 Hybrid Router (rule-based + LLM fallback)
- ⚡ Token optimization using deterministic routing
- 🔁 LangGraph conditional execution
- ☁ Deployable on Replit

---

## 🏗 Architecture

User  
↓  
Router Node (Deterministic Intent Detection)  
↓  
Conditional Edge  
↓  
Specialized Tool Node  
↓  
Final Response  

LangGraph is used instead of traditional AgentExecutor for:
- Controlled recursion
- Deterministic routing
- Production safety
- Cost optimization

---

## 🧰 Tech Stack

- Python 3.10+
- LangGraph
- LangChain Core
- Groq LLM (llama-3.1-8b / 70b)
- Pydantic
- OpenWeather API
- pytz / zoneinfo
- mongoDB
- rapidfuzz
- streamlit

---

## 📂 Project Structure
