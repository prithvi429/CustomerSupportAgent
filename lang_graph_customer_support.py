# lang_graph_customer_support.py
# Lang Graph Customer Support Agent with 11 stages

import logging
import random

logging.basicConfig(level=logging.INFO, format="%(message)s")

# -------------------------
# Dummy MCP Clients
# -------------------------
def call_common_server(ability, state):
    logging.info(f"[COMMON] Ability executed: {ability}")
    return {ability: f"common_result_for_{ability}"}

def call_atlas_server(ability, state):
    logging.info(f"[ATLAS] Ability executed: {ability}")
    return {ability: f"atlas_result_for_{ability}"}

def execute_ability(ability, server, state):
    if server == "COMMON":
        return call_common_server(ability, state)
    else:
        return call_atlas_server(ability, state)

# -------------------------
# Lang Graph Agent
# -------------------------
class LangGraphCustomerSupportAgent:
    def __init__(self):
        # Persistent state across stages
        self.state = {
            "customer": {},
            "intent": None,
            "priority": None,
            "ticket_status": "Open",
            "kb_answer": None,
            "solution_score": 0,
            "can_auto_solve": False,
            "reply": None,
            "logs": [],
        }

        # Stage Graph Definition
        self.stages = [
            {
                "name": "INTAKE",
                "mode": "deterministic",
                "abilities": [("accept_payload", "COMMON")]
            },
            {
                "name": "UNDERSTAND",
                "mode": "deterministic",
                "abilities": [("parse_request_text", "COMMON"), ("extract_entities", "ATLAS")]
            },
            {
                "name": "PREPARE",
                "mode": "deterministic",
                "abilities": [("normalize_fields", "COMMON"), ("enrich_records", "ATLAS"), ("add_flags_calculations", "COMMON")]
            },
            {
                "name": "ASK",
                "mode": "deterministic",
                "abilities": [("clarify_question", "ATLAS")]
            },
            {
                "name": "WAIT",
                "mode": "deterministic",
                "abilities": [("extract_answer", "ATLAS"), ("store_answer", "COMMON")]
            },
            {
                "name": "RETRIEVE",
                "mode": "deterministic",
                "abilities": [("knowledge_base_search", "ATLAS"), ("store_data", "COMMON")]
            },
            {
                "name": "DECIDE",
                "mode": "non-deterministic",
                "abilities": [("solution_evaluation", "COMMON"), ("escalation_decision", "ATLAS"), ("update_payload", "COMMON")]
            },
            {
                "name": "UPDATE",
                "mode": "deterministic",
                "abilities": [("update_ticket", "ATLAS"), ("close_ticket", "ATLAS")]
            },
            {
                "name": "CREATE",
                "mode": "deterministic",
                "abilities": [("response_generation", "COMMON")]
            },
            {
                "name": "DO",
                "mode": "deterministic",
                "abilities": [("execute_api_calls", "ATLAS"), ("trigger_notifications", "ATLAS")]
            },
            {
                "name": "COMPLETE",
                "mode": "deterministic",
                "abilities": [("output_payload", "COMMON")]
            },
        ]

    # -------------------------
    # Simple KB Search
    # -------------------------
    def knowledge_base_search(self, query):
        if "order" in query.lower():
            return "Your order is delayed due to shipping issues. Expected delivery in 3 days."
        elif "refund" in query.lower():
            return "Refunds are processed within 5-7 business days."
        elif "password" in query.lower():
            return "You can reset your password by clicking 'Forgot Password' on the login page."
        else:
            return None

    # -------------------------
    # Stage Execution
    # -------------------------
    def run(self, customer_info: dict):
        # Store payload upfront
        self.state["customer"] = customer_info
        self.state["priority"] = customer_info.get("priority", "normal")

        for stage in self.stages:
            stage_name = stage["name"]
            logging.info(f"\n--- STAGE: {stage_name} | Mode: {stage['mode']} ---")
            if stage_name == "RETRIEVE":
                # Retrieve KB answer
                query = self.state["customer"].get("query", "")
                kb_answer = self.knowledge_base_search(query)
                self.state["kb_answer"] = kb_answer
                logging.info(f"KB Answer Retrieved: {kb_answer}")

            for ability, server in stage["abilities"]:
                if stage_name == "DECIDE":
                    # Non-deterministic logic
                    if ability == "solution_evaluation":
                        if self.state["kb_answer"]:
                            self.state["solution_score"] = random.randint(90, 100)
                        else:
                            self.state["solution_score"] = random.randint(60, 80)
                        logging.info(f"Solution Evaluation Score: {self.state['solution_score']}")
                        # Decide auto-solve
                        self.state["can_auto_solve"] = self.state["solution_score"] >= 90
                    elif ability == "escalation_decision":
                        if not self.state["can_auto_solve"]:
                            logging.info("Escalation decision: Ticket escalated to human agent")
                            self.state["ticket_status"] = "Escalated"
                        else:
                            self.state["ticket_status"] = "Resolved"
                    elif ability == "update_payload":
                        logging.info(f"Payload updated with decision outcomes: Status={self.state['ticket_status']}")
                        continue  # No MCP call needed
                    else:
                        execute_ability(ability, server, self.state)
                else:
                    execute_ability(ability, server, self.state)

            # Special handling for CREATE stage
            if stage_name == "CREATE":
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
                logging.info(f"Reply drafted: {self.state['reply']}")

            # Special handling for COMPLETE stage
            if stage_name == "COMPLETE":
                final_payload = {
                    "ticket_id": self.state["customer"]["ticket_id"],
                    "status": self.state["ticket_status"],
                    "reply": self.state["reply"]
                }
                logging.info(f"Final Payload: {final_payload}")

        return final_payload

# -------------------------
# Demo Run
# -------------------------
if __name__ == "__main__":
    agent = LangGraphCustomerSupportAgent()

    customer_info = {
        "name": "Alice Smith",
        "email": "alice@example.com",
        "query": "I want a refund for my last order.",
        "priority": "high",
        "ticket_id": "TCK-1001"
    }

    result = agent.run(customer_info)
    print("\n=== FINAL OUTPUT ===")
    print(result)
