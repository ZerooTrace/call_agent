import os
from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID=os.getenv("twilio_account_sid")
TWILIO_AUTH_TOKEN=os.getenv("twiliao_auth_token")
GEMINI_API_KEY=os.getenv("gemini_api_key")
SARVAM_API_KEY=os.getenv("sarvam_api_key")