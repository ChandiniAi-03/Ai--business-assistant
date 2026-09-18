# 🤖 AI Business Assistant

An AI-powered business automation platform that monitors Gmail, identifies actionable information from emails, generates professional responses, extracts tasks, schedules meetings through Google Calendar, stores automation data in SQLite, and provides a web dashboard to monitor the entire workflow.

The project combines **AI, automation, APIs, databases, and web development** into one end-to-end business assistant.

---

## ✨ Features

### 📧 Intelligent Email Monitoring

* Connects securely to Gmail using the Gmail API.
* Reads recent emails and extracts relevant information.
* Tracks processed emails to prevent duplicate processing.

### 🧠 AI Email Analysis

* Uses a locally running **Llama 3.2 model through Ollama**.
* Identifies email intent such as:

  * Meeting requests
  * Tasks/action items
  * Response-required emails
  * General emails
* Detects urgency levels.

### ✍️ AI Response Generation

* Generates professional email responses based on the detected intent.
* Responses are stored in the SQLite database.
* The system does not automatically send generated responses, allowing them to be reviewed before sending.

### 📋 Task Automation

* Extracts actionable tasks from emails using AI.
* Identifies:

  * Task description
  * Priority
  * Due date
  * Status
* Saves tasks automatically to the database.
* Prevents previously processed emails from being processed again.

### 📅 Meeting Automation

* Detects meeting requests from emails.
* Extracts meeting information such as:

  * Meeting title
  * Date
  * Time
  * Duration
  * Description
* Creates events automatically in Google Calendar.
* Stores the created meeting and calendar link in SQLite.
* Includes duplicate-meeting protection.

### 🗄️ Database & Logging

Uses **SQLite** to store:

* Tasks
* Meetings
* AI-generated responses
* Processed email IDs
* Automation logs

This provides a persistent record of what the assistant has processed and what actions it performed.

### 🖥️ Automation Dashboard

A Flask-based web dashboard provides an overview of:

* Emails processed
* Action items detected
* Meetings scheduled
* AI responses generated
* Recent automation activity
* Tasks
* Scheduled meetings
* Automation logs

The dashboard also provides controls to run:

* Gmail scanning
* Meeting processing
* Full automation

---

## 🔄 How It Works

```text
                 ┌─────────────────┐
                 │      Gmail      │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Email Monitoring│
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │   AI Analysis   │
                 │   Llama 3.2     │
                 └────────┬────────┘
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
        ┌─────────┐ ┌──────────┐ ┌─────────────┐
        │  Tasks  │ │ Meetings │ │ AI Response │
        └────┬────┘ └─────┬────┘ └──────┬──────┘
             │            │              │
             │            ▼              │
             │    ┌──────────────┐      │
             │    │ Google       │      │
             │    │ Calendar API │      │
             │    └──────┬───────┘      │
             │           │              │
             └───────────┼──────────────┘
                         ▼
                  ┌─────────────┐
                  │   SQLite    │
                  │  Database   │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │ Flask Web   │
                  │  Dashboard  │
                  └─────────────┘
```

---

## 🛠️ Tech Stack

| Technology          | Purpose                                         |
| ------------------- | ----------------------------------------------- |
| Python              | Core application and automation logic           |
| Flask               | Web application and dashboard                   |
| Ollama              | Local AI model execution                        |
| Llama 3.2           | AI analysis, extraction and response generation |
| Gmail API           | Email monitoring                                |
| Google Calendar API | Meeting automation                              |
| SQLite              | Persistent data storage                         |
| HTML                | Dashboard structure                             |
| CSS                 | Dashboard styling                               |
| Jinja2              | Dynamic dashboard rendering                     |
| Google OAuth 2.0    | Secure Google API authentication                |

---

## 📂 Project Structure

```text
AI-business-Assistant/
│
├── app/
│   ├── automation/
│   │   ├── analyze_inbox.py
│   │   ├── email_analyzer.py
│   │   ├── email_monitor.py
│   │   ├── inbox_automation.py
│   │   ├── meeting_automation.py
│   │   ├── meeting_extractor.py
│   │   ├── response_generator.py
│   │   ├── task_automation.py
│   │   └── task_extractor.py
│   │
│   └── services/
│       ├── calendar_service.py
│       ├── database.py
│       └── gmail_service.py
│
├── data/
├── reports/
├── static/
│   └── css/
│       └── style.css
│
├── templates/
│   └── dashboard.html
│
├── tests/
│   ├── test_ai_response.py
│   ├── test_analyzer.py
│   ├── test_calendar.py
│   ├── test_database.py
│   ├── test_gmail.py
│   ├── test_meeting_automation.py
│   ├── test_meeting_extractor.py
│   └── test_task_extractor.py
│
├── .gitignore
├── app.py
├── requirements.txt
└── README.md
```

> Sensitive authentication files such as Google credentials, OAuth tokens, environment variables, the virtual environment, and the local SQLite database are intentionally excluded from version control.

---

## 🔐 Security

The project uses Google OAuth authentication rather than storing Gmail or Calendar passwords directly.

Sensitive files are excluded through `.gitignore`, including:

```text
credentials/
token.json
calendar_token.json
.env
venv/
data/assistant.db
```

**Never upload Google API credentials, OAuth tokens, passwords, API keys, or personal email data to GitHub.**

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd AI-business-Assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Google APIs

Create a Google Cloud project and enable:

* Gmail API
* Google Calendar API

Create OAuth desktop credentials and place the credentials file inside:

```text
credentials/credentials.json
```

The Google account used for testing must be authorized according to the OAuth application's configuration.

### 5. Install and run Ollama

Install Ollama and download the model:

```bash
ollama pull llama3.2
```

Make sure Ollama is running locally.

### 6. Start the Flask application

```bash
python app.py
```

Open the local dashboard in a browser:

```text
http://127.0.0.1:5000
```

---

## ▶️ Automation Controls

The dashboard provides three main automation actions:

### 🔄 Scan Gmail

Scans recent Gmail messages and processes new emails.

### 📅 Process Meetings

Looks for meeting requests and creates corresponding Google Calendar events.

### 🧠 Run Full Automation

Runs the complete business workflow, including inbox processing and meeting automation.

---

## 🧪 Testing

The project includes separate test scripts covering major components such as:

* Gmail integration
* Calendar integration
* Database operations
* Email analysis
* AI response generation
* Meeting extraction
* Meeting automation
* Task extraction

Example:

```bash
python tests/test_task_extractor.py
```

---

## 💡 Key Learning Outcomes

This project was built to gain practical experience with:

* AI-powered workflow automation
* Local LLM integration
* Prompt engineering
* Gmail API integration
* Google Calendar API integration
* OAuth authentication
* REST/API-based services
* Database design with SQLite
* Flask web development
* Automation pipelines
* Error handling
* Duplicate prevention
* Logging and monitoring
* Building an end-to-end AI application

---

## 🚀 Future Improvements

Potential future enhancements include:

* Automatic email response sending with user approval
* More advanced email classification
* Background/scheduled automation
* Recurring task management
* Calendar availability checking
* Weekly AI-generated business reports
* Email and task analytics
* User authentication
* Production cloud deployment
* More advanced dashboard visualizations

---

## 👩‍💻 Project Focus

This project demonstrates the practical use of **AI + automation + APIs + web development** to reduce repetitive business tasks and create an intelligent workflow assistant.

**Built as an AI automation engineering project.**
