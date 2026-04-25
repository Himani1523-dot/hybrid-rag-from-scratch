# 🤖 Chatbot Project Notes

##  Model Used
- Model: Phi-3 Mini Instruct 
- Source: LM Studio
- Runs locally (no API key needed)
- Endpoint: http://localhost:1234

---

##  Setup
- Installed LM Studio
- Downloaded model (GGUF format)
- Started Local Server in LM Studio

---

##  Code Files

### 1. app.py (Stateless Chatbot)
- No memory
- Each request is independent
- Does NOT remember previous conversation

Example:
User: My name is Rahul  
Bot: (responds)  
User: What is my name?  
Bot:  Does not remember  

---

### 2. memory.py (Stateful Chatbot)
- Uses `conversation` list
- Stores user + assistant messages
- Sends full history every time

Example:
User: My name is Rahul  
Bot: OK  
User: What is my name?  
Bot: ✅ Remembers  

---
