import os
from fastapi import FastAPI, Request, Response
from fastapi.responses import PlainTextResponse
from twilio.twiml.voice_response import VoiceResponse, Gather

import requests
import config
from google import genai

app = FastAPI()

client = genai.Client()

SARVAM_API_KEY=config.SARVAM_API_KEY

# Maan lo aapke paas aisi list hai
past_chats = []

def generate_gemini_response(user_speech: str) -> str:
    # Dictionary ki list ko clean string loop mein convert kiya taaki .join() crash na kare
    history_text = "\n".join([f"{chat['role']}: {chat['message']}" for chat in past_chats])

    # 1. Pehle User ka chat append karo
    past_chats.append({"role": "user", "message": user_speech})
    
    # Prompt ke andar string formatting se fit kar do
    prompt = f"""
    You are a phone assistant. Here is the context of past conversation:
    {history_text}
    
    Now the caller says: {user_speech}
    Please reply in less than 2 sentences.
    """
    
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite', # Version code clean aur stable rakha
        contents=prompt,
    )
    
    # 2. Phir Assistant ka chat append karo
    past_chats.append({"role": "assistant", "message": response.text})
    return response.text

def get_sarvam_tts_url(text: str):
    """Uses Sarvam AI to turn text into a natural Indian voice file."""
    # Note: Sarvam's standard endpoint or audio hosting link is used here.
    # In a produntion streaming system, You'd feed this via a webSocket audio stream.
    url = "https://api.sarvam.ai/text-to-speech"
    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "content-Type": "application/json"
    }
    payload = {
        "text": text,
        "target_language_code": "hi-IN",
        "speaker": "meera",
        "model": "bulbul:v3"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        # assuming Sarvam returns an audio url or you pipe the raw audio bytes
        # to a public static bucket.
        return response.json().get("audio_url")
    except:
        return ""
    
    
@app.post("/voice")
async def handle_incoming_call():
    """triggered when someone dials your twilio number."""
    vr = VoiceResponse()

    # Gather listens to the caller, transcribes it, and sends it to /respond
    gather = Gather(input='speech', action='/respond', speechTimeout='auto')
    gather.say("Hello! Thanks for calling. How can I help you today?", voice="Polly.Aditi")
    vr.append(gather)

    # IF the user stays silent
    vr.say("I didn't catch that. Goodbye!")
    return Response(content=str(vr), media_type="application/xml")

@app.post("/respond")
async def handle_response(request: Request):
    """process what the user said, requests Gemini, uses Sarvam, and replies."""
    form_data = await request.form()
    user_speech = form_data.get("SpeechResult", "")

    vr = VoiceResponse()

    if user_speech:
        # 1. Get text from gemini
        ai_reply = generate_gemini_response(user_speech)

        

        # Get audio from sarvam AI 
        audio_url = get_sarvam_tts_url(ai_reply)

        if audio_url: 
            # play sarvam's hyper-realistic localized audio voice over the phone
            vr.play(audio_url)
        else:
            # Fallback text-to-speech if the sarvam endpoint fails.
            vr.say(ai_reply, voice="Polly.Aditi")

        gather = Gather(input='speech', action='/respond', speechTimeout='auto')
        vr.append(gather)
    
    else:
        vr.say("Are you still there ? please say something.")
        gather = Gather(input='speech', action='/respond', speechTimeout='auto')
        vr.append(gather)

    return Response(content=str(vr), media_type="application/xml")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)