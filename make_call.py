from twilio.rest import Client
import os
import config

# Twilio Credentials

account_sid = config.TWILIO_ACCOUNT_SID
auth_token = config.TWILIO_AUTH_TOKEN
client = Client(account_sid, auth_token)

# Ngrok URL jo aapne setup kiya tha
ngrok_url = " https://create-your-ngrok-tunnel.ngrok-free.dev/voice"

call = client.calls.create(
    url=ngrok_url,                       # Aapka FastAPI endpoint
    to='+917248XXXX74',                 # Aapka apna verified Indian number
    from_='+14787XXXX78'                # Aapka Twilio Trial Number
)

print(f"Call initiate ho gayi hai! SID: {call.sid}")