import streamlit as st
from customer_support_agent import CustomerSupportAgent

st.title("🧩 Customer Support Agent Demo")

# Collect customer details
name = st.text_input("Customer Name")
email = st.text_input("Customer Email")
query = st.text_area("Customer Query")
priority = st.selectbox("Priority", ["low", "medium", "high"])
ticket_id = st.text_input("Ticket ID")

if st.button("Run Agent"):
    customer_info = {
        "name": name,
        "email": email,
        "query": query,
        "priority": priority,
        "ticket_id": ticket_id
    }

    agent = CustomerSupportAgent()
    result = agent.run(customer_info)

    st.subheader("🔄 Final Result")
    st.json(result)
