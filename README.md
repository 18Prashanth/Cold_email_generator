# Cold_email_generator

This repository contains the source code related to cold email generator project.
📧 Cold Email Generator App
This is a full-stack AI-powered cold email generator. Users submit a job posting link, and the backend (FastAPI) generates a tailored cold email using an LLM and sends it back to the frontend interface.

### 🚀 Features

🔗 Submit a job link (e.g., from LinkedIn, Indeed, or Oracle Careers).

🤖 Automatically generate a personalized cold email.

💡 Uses an LLM (e.g., LLaMA3) to create context-aware messages.

🌐 Clean, modern frontend built with HTML, CSS & JavaScript.

⚡ FastAPI backend with JSON API.

📨 Ready for deployment via server or AWS Lambda + API Gateway.

### 🛠️ Tech Stack

Frontend: HTML, CSS, JavaScript

Backend: FastAPI (Python)

LLM: Meta’s LLaMA3 or any API-compatible model (e.g., OpenAI, Bedrock)

Deployment Options: Localhost / EC2 / AWS Lambda + API Gateway

### 📁 Project Structure

```
cold_email/
│
├── app/
│ ├── main.py # FastAPI entrypoint
│ ├── routers/
│ │ └── coldemail.py # Route to process link and generate email
│ ├── utils/
│ └── email_utils.py # Core email generation logic
├── templates/
│ └── index.html # HTML frontend
├── static/
│ ├── style.css # CSS styles
│ └── app.js # JS logic (fetch & render)
├── vectorstore/
├── venv/ # Python virtual environment (ignored)
├── README.md # Project documentation
├── requirements.txt # Python dependencies
```

### 📦 Setup & Run Locally

# Clone the repository

```
git clone https://github.com/your-username/cold-email-generator.git
cd cold-email-generator
```

# Create and activate virtual environment

```
python -m venv venv
venv\Scripts\activate # on Windows
```

# Install dependencies

```
pip install -r requirements.txt
```

# Run the FastAPI app

```
uvicorn app.main:app --reload
```

# 🖥️ Access Frontend

Open your browser and go to:

http://localhost:8000/

Paste any job posting link and click "Generate Email" 💌

# 📜 License

MIT License - Free to use and modify.

## 💡 Author

Prashanth Gowda A S

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?logo=linkedin)](https://www.linkedin.com/in/prashanthgowdaas/)
