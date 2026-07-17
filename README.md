# 🎙️ Multi-lingual AI Voice Calling Agent

An intelligent, multi-lingual voice calling agent that pairs **Twilio Virtual Numbers**, **Google Gemini** (for brain & context processing), and **Sarvam AI** (for realistic, native Indian accents and text-to-speech) to create seamless, automated phone conversations.

This repository uses a custom global history tracker to persist context, allowing the model to naturally reference past statements during live telephonic interaction.

---

## 🏗️ Architecture Workflow

1. **User Speaks**: User dials/receives a call via Twilio.
2. **Audio Streaming**: Twilio captures the user audio, transcribes it on-the-fly (`Gather`), and streams the data to your local machine via an **ngrok** tunnel.
3. **Contextual Processing**: Your FastAPI server receives the user text, appends it to a global context list, and builds an aggregate prompt for the **Google Gemini API**.
4. **Natural Speech Synthesis**: The text response from Gemini is dispatched to **Sarvam AI's Bulbul:v3 engine** to generate hyper-realistic audio matching native regional styles (such as Hinglish/Hindi).
5. **Playback**: Twilio fetches the generated audio track URL and plays it seamlessly back to the listener.

---

## 🛠️ Tech Stack & Requirements

- **Backend Framework**: Python 3.10+ / FastAPI / Uvicorn
- **Telephony Pipeline**: Twilio API & TwiML (`twilio-python`)
- **LLM Context Engine**: Google GenAI SDK (`google-genai`)
- **Voice Synthesis**: Sarvam AI Text-To-Speech API
- **Web Tunneling**: Ngrok

---

## 🚀 Complete Step-by-Step Setup Guide

Follow these exact steps to configure and run the project on your local machine (PC/Laptop):

### Step 1: Clone or Download the Project
Open your terminal (PowerShell on Windows, or Terminal on Mac/Linux) and run:
```bash
git clone [https://github.com/YOUR_USERNAME/your-repo-name.git](https://github.com/YOUR_USERNAME/your-repo-name.git)
cd your-repo-name
(If you downloaded the code as a ZIP file, extract it and open your terminal inside that extracted folder).

Step 2: Create a Virtual Environment (Isolated Environment)
To avoid any package conflicts with your system's global Python settings, create a virtual environment inside your project directory:

On Windows (PowerShell):

PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
On macOS / Linux:

Bash
python3 -m venv venv
source venv/bin/activate
Once activated, you will see (venv) at the beginning of your terminal line.

Step 3: Install Required Dependencies
Run this command to install all the required tools, frameworks, and API clients inside your environment:

Bash
pip install fastapi uvicorn twilio google-genai requests python-multipart
Step 4: Configure API Credentials & Keys
You need to create a config file for Sarvam AI and set an environment variable for Gemini.

For Sarvam AI: Create a new file named config.py in the root folder and paste your key like this:

Python
# config.py
SARVAM_API_KEY = "your_actual_sarvam_api_key_here"
For Google Gemini (Environment Variable): Set your Gemini API token directly into your active terminal session:

On Windows (PowerShell):

PowerShell
$env:GEMINI_API_KEY="your_actual_gemini_api_key_here"
On macOS / Linux:

Bash
export GEMINI_API_KEY="your_actual_gemini_api_key_here"
🌐 Public Tunnel Routing (Ngrok Setup)
Twilio runs on the cloud, so it cannot access your localhost:8000 directly. You must open a secure public tunnel using ngrok:

Download and install Ngrok.

Run this command in a separate terminal window:

Bash
ngrok http 8000
Look at the terminal screen and copy the secure URL starting with https:// (e.g., https://xxxx-xxxx.ngrok-free.app). Keep this terminal window running.

📞 Twilio Webhook Configuration
Bypass ISD Block For Trial Accounts
If you are using a Twilio Free Trial Account, standard outgoing international calls might be blocked on Indian SIM networks.

Log into your Twilio Console.

Go to Phone Numbers -> Manage -> Verified Caller IDs.

Click Add a New Caller ID and register your target mobile phone number (+91XXXXXXXXXX) via OTP/Call.

Point Twilio to Your Local Code
In your Twilio Dashboard, click on your active virtual phone number.

Scroll down to the Voice & Fax section.

Under "A Call Comes In", select Webhook and choose HTTP POST.

Paste your Ngrok secure URL followed by /voice:

Plaintext
[https://your-ngrok-subdomain.ngrok-free.app/voice](https://your-ngrok-subdomain.ngrok-free.app/voice)
Click Save at the bottom of the page.

🏃 Running the Application
Go back to your main terminal (where your python environment (venv) is active) and start your FastAPI server:

Bash
python app.py
Dial your Twilio virtual number from your verified phone.

Talk natively (use Hindi or English). The server logs will display your conversations dynamically, and you will hear real-time localized voice replies from Sarvam AI!

📁 File Structure
Plaintext
├── app.py          # Main FastAPI server handling webhook audio logic
├── config.py       # Secret credentials holding Sarvam AI tokens (Git-ignored)
├── README.md       # Step-by-step documentation
└── venv/           # Python virtual environment directory

Ab is content ko file mein daal kar push kar do, koi bhi ise easily read karke set kar lega!
