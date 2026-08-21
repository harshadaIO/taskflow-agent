import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types

load_dotenv()

# Define the tools
def log_invoice_to_file(vendor: str, amount: str, description: str, email: str) -> str:
    """Logs an approved invoice to a local text file database."""
    log_entry = f"VENDOR: {vendor} | AMOUNT: {amount} | FOR: {description} | EMAIL: {email}\n"
    with open("invoice_database.txt", "a") as f:
        f.write(log_entry)
    return f"Success! Invoice for {vendor} amounting to {amount} has been logged."

def send_confirmation_email(email: str, vendor: str, amount: str) -> str:
    """Sends a mock confirmation email to the billing department of the vendor."""
    email_record = f"TO: {email} | SUBJECT: Invoice Received | BODY: Hello {vendor}, we received your invoice for {amount} and it is being processed.\n"
    with open("email_outbox.txt", "a") as f:
        f.write(email_record)
    return f"Success! Confirmation email dispatched to {email}."

# Setup Agent
root_agent = Agent(
    name="taskflow_master",
    model="gemini-3.6-flash",
    description="An autonomous operations agent that processes workflows, logs invoices, and sends emails.",
    instruction=(
        "You are an expert operations assistant. When given an invoice task, you MUST do two things: "
        "1. Call the log_invoice_to_file tool. "
        "2. Call the send_confirmation_email tool. "
        "After both tools execute successfully, provide a clear summary."
    ),
    tools=[log_invoice_to_file, send_confirmation_email]
)

# Streamlit UI Configuration
st.set_page_config(page_title="TaskFlow AI Agent", page_icon="⚡", layout="centered")

st.title("⚡ TaskFlow AI: Autonomous Operations Agent")
st.markdown("Powered by **Google ADK & Gemini** 🚀. Type your messy workflow or invoice request below:")

user_input = st.text_area("Enter your task request:", "Hey, I need to process an invoice from Acme Corp for $450. It's for cloud hosting, date was yesterday, send a confirmation email to billing@acmecorp.com and log it.")

if st.button("🚀 Run Agent Workflow"):
    if not user_input.strip():
        st.warning("Please enter a valid task.")
    else:
        with st.spinner("Agent is processing and executing tools..."):
            try:
                # Run the async agent runner inside Streamlit
                async def run_agent():
                    session_service = InMemorySessionService()
                    runner = Runner(
                        agent=root_agent,
                        app_name="taskflow_app",
                        session_service=session_service
                    )
                    session_id = "streamlit_session"
                    await session_service.create_session(app_name="taskflow_app", user_id="user_1", session_id=session_id)
                    
                    content = types.Content(role="user", parts=[types.Part(text=user_input)])
                    
                    response_text = "No response generated."
                    async for event in runner.run_async(session_id=session_id, user_id="user_1", new_message=content):
                        if hasattr(event, 'content') and event.content and event.content.parts:
                            text_parts = [p.text for p in event.content.parts if p.text]
                            if text_parts:
                                response_text = "".join(text_parts)
                    return response_text

                agent_output = asyncio.run(run_agent())
                
                st.success("Workflow executed successfully!")
                st.markdown("### 📤 Agent Response:")
                st.write(agent_output)
                
                # Show file outputs for hackathon proof
                if os.path.exists("invoice_database.txt"):
                    with st.expander("📁 View Database Logs"):
                        with open("invoice_database.txt", "r") as f:
                            st.text(f.read())
                            
            except Exception as e:
                st.error(f"An error occurred: {e}")