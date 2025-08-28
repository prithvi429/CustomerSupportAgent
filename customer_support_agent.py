# customer_support_agent.py
# Customer Support Agent that accepts full customer info

import logging
import random

logging.basicConfig(level=logging.INFO, format="%(message)s")

stages = [
    {"name": "INTAKE", "mode": "deterministic", "abilities": [("accept_payload", "COMMON")]},
    {"name": "UNDERSTAND", "mode": "deterministic", "abilities": [("parse_request_text", "COMMON"), ("extract_entities", "ATLAS")]},
    {"name": "PREPARE", "mode": "deterministic", "abilities": [("normalize_fields", "COMMON"), ("enrich_records", "ATLAS"), ("add_flags_calculations", "COMMON")]},
    {"name": "DECIDE", "mode": "non-deterministic", "abilities": [("solution_evaluation", "COMMON"), ("escalation_decision", "ATLAS")]}
]

# Dummy MCP Clients
def call_common_server(ability, state):
    logging.info(f"[COMMON] {ability} executed")
    return {ability: f"common_result_for_{ability}"}

def call_atlas_server(ability, state):
    logging.info(f"[ATLAS] {ability} executed")
    return {ability: f"atlas_result_for_{ability}"}

def execute_ability(ability, server, state):
    if server == "COMMON":
        return call_common_server(ability, state)
    else:
        return call_atlas_server(ability, state)

class CustomerSupportAgent:
    def __init__(self):
        self.state = {
            "customer": {},
            "priority": None,
            "ticket_status": "Open",
            "kb_answer": None,
            "solution_score": 0,
            "can_auto_solve": False,
            "reply": None,
            "logs": []
        }

    # Simple knowledge base
    def knowledge_base_search(self, query):
        if "order" in query.lower():
            return "Your order is delayed due to shipping issues. Expected delivery in 3 days."
        elif "refund" in query.lower():
            return "Refunds are processed within 5-7 business days."
        elif "password" in query.lower():
            return "You can reset your password by clicking 'Forgot Password' on the login page."
        else:
            return None

    # Full workflow
    def run(self, customer_info: dict):
        # Stage 1: INTAKE
        self.state["customer"] = customer_info
        logging.info(f"INTAKE: {self.state['customer']}")

        # Stage 2: UNDERSTAND (rule-based intent extraction)
        query = customer_info.get("query", "")
        if "order" in query.lower():
            self.state["intent"] = "delivery_issue"
        elif "refund" in query.lower():
            self.state["intent"] = "refund_request"
        elif "password" in query.lower():
            self.state["intent"] = "account_issue"
        else:
            self.state["intent"] = "general_query"
        logging.info(f"UNDERSTAND: intent={self.state['intent']}")

        # Stage 3: PREPARE
        execute_ability("normalize_fields", "COMMON", self.state)
        execute_ability("enrich_records", "ATLAS", self.state)
        execute_ability("add_flags_calculations", "COMMON", self.state)
        logging.info(f"PREPARE: Priority={customer_info.get('priority')}")

        # Stage 4: ASK (skipped)
        logging.info("ASK: No clarification needed")

        # Stage 5: WAIT (skipped)
        logging.info("WAIT: No pending answer")

        # Stage 6: RETRIEVE
        self.state["kb_answer"] = self.knowledge_base_search(query)
        execute_ability("knowledge_base_search", "ATLAS", self.state)
        logging.info(f"RETRIEVE: KB Answer={self.state['kb_answer']}")

        # Stage 7: DECIDE
        if self.state["kb_answer"]:
            self.state["solution_score"] = random.randint(90, 100)
        else:
            self.state["solution_score"] = random.randint(60, 80)

        if self.state["solution_score"] >= 90:
            self.state["can_auto_solve"] = True
            execute_ability("solution_evaluation", "COMMON", self.state)
            self.state["ticket_status"] = "Resolved"
        else:
            self.state["can_auto_solve"] = False
            execute_ability("escalation_decision", "ATLAS", self.state)
            self.state["ticket_status"] = "Escalated"
        logging.info(f"DECIDE: score={self.state['solution_score']} auto_solve={self.state['can_auto_solve']}")

        # Stage 8: UPDATE
        execute_ability("update_ticket", "ATLAS", self.state)
        logging.info(f"UPDATE: Ticket status={self.state['ticket_status']}")

        # Stage 9: CREATE
        if self.state["can_auto_solve"]:
            self.state["reply"] = (
                f"Hello {self.state['customer']['name']},\n"
                f"{self.state['kb_answer']}\n"
                "Thank you for your patience."
            )
        else:
            self.state["reply"] = (
                f"Hello {self.state['customer']['name']},\n"
                "Your issue has been escalated to our support team."
            )
        logging.info("CREATE: Reply drafted")

        # Stage 10: DO
        execute_ability("trigger_notifications", "ATLAS", self.state)
        logging.info("DO: Notifications sent")

        # Stage 11: COMPLETE
        final_payload = {
            "ticket_id": self.state["customer"]["ticket_id"],
            "status": self.state["ticket_status"],
            "reply": self.state["reply"]
        }
        logging.info(f"COMPLETE: {final_payload}")
        return final_payload


if __name__ == "__main__":
    agent = CustomerSupportAgent()

    customer_info = {
        "name": "Alice Smith",
        "email": "alice@example.com",
        "query": "I want a refund for my last order.",
        "priority": "high",
        "ticket_id": "TCK-1001"
    }

    result = agent.run(customer_info)
    print("\nFINAL OUTPUT:")
    print(result)
