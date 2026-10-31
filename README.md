# ⚡ TaskFlow AI: Autonomous Operations Agent

> **TaskFlow AI** is an autonomous, multi-tool operations agent built using **Google's Agent Development Kit (ADK)** and powered by **Gemini**. It turns messy, unstructured natural language requests into structured business execution automatically extracting data, logging records to a database, and dispatching communications.

---

## 🌟 Key Features

* **Natural Language Parsing:** Takes unstructured inputs (e.g., messy emails or Slack messages about invoices) and cleanly extracts key entities like vendors, amounts, descriptions, and contacts.
* **Autonomous Tool-Use:** Dynamically invokes custom Python functions to write persistent records (`invoice_database.txt`) and send confirmations (`email_outbox.txt`).
* **Interactive Web Interface:** Built using **Streamlit**, providing a sleek, dark-mode user interface for live demos and real-time verification.
* **Stateful Sessions:** Powered by Google ADK’s session and memory management framework.

---

## 🛠️ Tech Stack

* **Framework:** Google Agent Development Kit (ADK)
* **LLM:** Gemini (via Google GenAI SDK)
* **Frontend:** Streamlit
* **Language:** Python

---

## 🚀 Getting Started Locally

Follow these steps to set up and run TaskFlow AI on your machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/taskflow-agent.git](https://github.com/your-username/taskflow-agent.git)
cd taskflow-agent
