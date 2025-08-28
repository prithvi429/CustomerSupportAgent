# customer_support_agent.py
# Customer Support Agent: Step-by-step flow with LLM-enhanced UNDERSTAND stage
import openai

# Set your OpenAI API key here (replace with your actual key)
openai.api_key = "your-api-key"

class Node:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.next_nodes = []
    def add_next(self, node, condition=None):
        self.next_nodes.append((node, condition))
    def __repr__(self):
        return f"Node({self.name})"

class CustomerSupportAgent:
    def __init__(self):
        # Define nodes
        self.intake = Node("INTAKE", "Accept customer details")
        self.understand = Node("UNDERSTAND", "Interpret the query meaning")
        self.prepare = Node("PREPARE", "Clean data, check ticket history, add priority flags")
        self.ask = Node("ASK", "Request missing info from customer if needed")
        self.wait = Node("WAIT", "Wait for customer reply and store it")
        self.retrieve = Node("RETRIEVE", "Search knowledge base for answers")
        self.decide = Node("DECIDE", "Decide auto-solve or escalate")
        self.update = Node("UPDATE", "Update ticket status")
        self.create = Node("CREATE", "Draft reply to customer")
        self.do = Node("DO", "Run actions (send notifications, call APIs)")
        self.complete = Node("COMPLETE", "Output final structured result")
        # State
        self.state = {
            'customer': {},
            'issue_type': None,
            'ticket_history': [],
            'priority': 'normal',
            'missing_info': [],
            'kb_result': None,
            'auto_solve': False,
            'ticket_status': None,
            'reply': None,
            'actions': [],
            'final_result': None
        }

    def intake_stage(self, details):
        self.state['customer'] = details
        print(f"INTAKE: Received details {details}")

    def understand_with_llm(self, query):
        """
        Use OpenAI LLM to classify the customer query.
        Returns a string label (e.g., 'late delivery', 'refund request', etc.)
        """
        prompt = (
            "Classify the following customer support query into an issue type (e.g., 'late delivery', 'refund request', 'product defect', 'cancellation', 'general inquiry'). "
            f"Query: {query}\nIssue type:"
        )
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=10,
                temperature=0
            )
            issue_type = response.choices[0].text.strip().lower()
            if not issue_type:
                raise ValueError("Empty LLM response")
            return issue_type
        except Exception as e:
            # Fallback: simple keyword matching
            q = query.lower()
            if "late" in q or "not arrived" in q:
                return "late delivery"
            elif "refund" in q:
                return "refund request"
            elif "defect" in q or "broken" in q:
                return "product defect"
            elif "cancel" in q:
                return "cancellation"
            else:
                return "general inquiry"

    def understand_stage(self):
        query = self.state['customer'].get('query', '')
        issue_type = self.understand_with_llm(query)
        self.state['issue_type'] = issue_type
        print(f"UNDERSTAND: Issue type identified as '{issue_type}'")

    def prepare_stage(self):
        # Simulate ticket history and priority
        self.state['ticket_history'] = ["Order placed", "Payment confirmed"]
        if self.state['issue_type'] == 'late delivery':
            self.state['priority'] = 'high'
        print(f"PREPARE: Ticket history {self.state['ticket_history']}, priority {self.state['priority']}")

    def ask_stage(self):
        # Check for missing info (simulate)
        missing = []
        for field in ['name', 'email', 'query', 'ticket_id']:
            if not self.state['customer'].get(field):
                missing.append(field)
        self.state['missing_info'] = missing
        if missing:
            print(f"ASK: Missing info {missing}, requesting from customer")
        else:
            print("ASK: All required info present")

    def wait_stage(self):
        if self.state['missing_info']:
            # Simulate waiting and receiving info
            print("WAIT: Waiting for customer reply...")
            # For demo, auto-fill missing info
            for field in self.state['missing_info']:
                self.state['customer'][field] = f"dummy_{field}"
            print(f"WAIT: Received missing info {self.state['missing_info']}")
        else:
            print("WAIT: No missing info, proceeding")

    def retrieve_stage(self):
        # Simulate KB search
        print("RETRIEVE: Searching knowledge base for solutions")
        self.state['kb_result'] = "Order is delayed due to shipping issues. Expected delivery in 3 days."

    def decide_stage(self):
        # Simulate auto-solve decision
        if self.state['issue_type'] == 'late delivery':
            self.state['auto_solve'] = True
            print("DECIDE: Auto-solving the issue")
        else:
            self.state['auto_solve'] = False
            print("DECIDE: Escalating to human agent")

    def update_stage(self):
        if self.state['auto_solve']:
            self.state['ticket_status'] = 'Resolved'
        else:
            self.state['ticket_status'] = 'Escalated'
        print(f"UPDATE: Ticket status updated to '{self.state['ticket_status']}'")

    def create_stage(self):
        # Draft reply
        name = self.state['customer'].get('name', 'Customer')
        reply = (
            f"Hello {name},\n"
            f"{self.state['kb_result']}\n"
            "Thank you for your patience."
        )
        self.state['reply'] = reply
        print(f"CREATE: Drafted reply:\n{reply}")

    def do_stage(self):
        # Simulate sending reply/notifications
        print("DO: Sending reply and notifications")
        self.state['actions'].append('sent_reply')

    def complete_stage(self):
        result = {
            'ticket_id': self.state['customer'].get('ticket_id'),
            'status': self.state['ticket_status'],
            'reply': self.state['reply']
        }
        self.state['final_result'] = result
        print(f"COMPLETE: Final result {result}")

    def run(self, customer_details):
        self.intake_stage(customer_details)
        self.understand_stage()
        self.prepare_stage()
        self.ask_stage()
        self.wait_stage()
        self.retrieve_stage()
        self.decide_stage()
        self.update_stage()
        self.create_stage()
        self.do_stage()
        self.complete_stage()


if __name__ == "__main__":
    # Example customer query
    customer = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'query': "My order #1234 hasn’t arrived.",
        'ticket_id': '1234'
    }
    agent = CustomerSupportAgent()
    agent.run(customer)
