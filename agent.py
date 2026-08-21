import os
import asyncio
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types

load_dotenv()

# Tool 1: Log invoice to file
def log_invoice_to_file(vendor: str, amount: str, description: str, email: str) -> str:
    """Logs an approved invoice to a local text file database."""
    log_entry = f"VENDOR: {vendor} | AMOUNT: {amount} | FOR: {description} | EMAIL: {email}\n"
    with open("invoice_database.txt", "a") as f:
        f.write(log_entry)
    return f"Success! Invoice for {vendor} amounting to {amount} has been logged."

# Tool 2: Send mock confirmation email
def send_confirmation_email(email: str, vendor: str, amount: str) -> str:
    """Sends a mock confirmation email to the billing department of the vendor."""
    email_record = f"TO: {email} | SUBJECT: Invoice Received | BODY: Hello {vendor}, we received your invoice for {amount} and it is being processed.\n"
    with open("email_outbox.txt", "a") as f:
        f.write(email_record)
    return f"Success! Confirmation email dispatched to {email}."

# Initialize agent with BOTH tools
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

async def main():
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="taskflow_app",
        session_service=session_service
    )
    
    session_id = "session_001"
    await session_service.create_session(app_name="taskflow_app", user_id="user_1", session_id=session_id)
    
    sample_messy_input = "Hey, I need to process an invoice from Acme Corp for $450. It's for cloud hosting, date was yesterday, send a confirmation email to billing@acmecorp.com and log it."
    
    print(f"📥 Input Task:\n{sample_messy_input}\n")
    print("⏳ Agent is processing and executing multiple tools...\n")
    
    content = types.Content(role="user", parts=[types.Part(text=sample_messy_input)])
    
    final_response = "Agent did not produce a final response."
    async for event in runner.run_async(session_id=session_id, user_id="user_1", new_message=content):
        if hasattr(event, 'content') and event.content and event.content.parts:
            text_parts = [p.text for p in event.content.parts if p.text]
            if text_parts:
                final_response = "".join(text_parts)
                
    print(f"📤 Agent Response:\n{final_response}")

if __name__ == "__main__":
    asyncio.run(main())