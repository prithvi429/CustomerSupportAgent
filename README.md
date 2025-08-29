
# 💡 CustomerSupportAgent

> **A modular, LangGraph-inspired AI workflow for customer support automation.**

---

## 🚀 Features
- **11 Structured Stages:** Step-by-step flow from intake to completion
- **Stateful:** Preserves customer/ticket state across all stages
- **MCP Integration:** Calls dummy MCP clients for abilities
- **LLM Ready:** Easily integrates OpenAI or other LLMs for smart intent understanding
- **Semantic KB Search:** (Optional) Add ChromaDB for FAQ/knowledge base retrieval
- **Auto-Escalation:** Decides when to escalate to a human agent

---

## 🛠️ Quick Start

1. **Clone this repo and open in VS Code**
2. **Install requirements** (if using LLM/ChromaDB):
   ```bash
   pip install openai chromadb
   ```
3. **Edit your imports**
   At the top of `customer_support_agent.py`:
   ```python
   import logging
   import random
   # from openai import OpenAI  # Uncomment if using LLM
   # import chromadb            # Uncomment if using ChromaDB
   ```
4. **Run the agent**
   ```bash
   python customer_support_agent.py
   ```

---

## 🧩 Stages Overview
| Stage        | Mode             | Abilities (Server)                                 |
|--------------|------------------|----------------------------------------------------|
| INTAKE       | Deterministic    | accept_payload (COMMON)                            |
| UNDERSTAND   | Deterministic    | parse_request_text (COMMON), extract_entities (ATLAS) |
| PREPARE      | Deterministic    | normalize_fields (COMMON), enrich_records (ATLAS), add_flags_calculations (COMMON) |
| ASK          | Deterministic    | clarify_question (ATLAS)                           |
| WAIT         | Deterministic    | extract_answer (ATLAS), store_answer (COMMON)      |
| RETRIEVE     | Deterministic    | knowledge_base_search (ATLAS), store_data (COMMON) |
| DECIDE       | Non-deterministic| solution_evaluation (COMMON), escalation_decision (ATLAS), update_payload (COMMON) |
| UPDATE       | Deterministic    | update_ticket (ATLAS), close_ticket (ATLAS)        |
| CREATE       | Deterministic    | response_generation (COMMON)                       |
| DO           | Deterministic    | execute_api_calls (ATLAS), trigger_notifications (ATLAS) |
| COMPLETE     | Deterministic    | output_payload (COMMON)                            |

---

## 🎬 Demo Video

Watch a quick demo of CustomerSupportAgent in action:

👉 [Demo Video on YouTube](https://www.youtube.com/watch?v=dQw4w9WgXcQ)

*Replace the link above with your own demo video if available.*

---

## 📝 Example Usage
```python
from customer_support_agent import CustomerSupportAgent

agent = CustomerSupportAgent()
customer_info = {
    "name": "Alice Smith",
    "email": "alice@example.com",
    "query": "I want a refund for my last order.",
    "priority": "high",
    "ticket_id": "TCK-1001"
}
result = agent.run(customer_info)
print(result)
```

---

## 📦 Extending
- Swap in your own LLM or KB search logic
- Connect to real MCP/Atlas APIs
- Add more stages or custom business logic

---

## 📚 License
MIT
