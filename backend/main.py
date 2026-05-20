import os
import httpx
from pathlib import Path
from fastapi import FastAPI, Body, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

env_path = Path('/home/utee/Documents/ExMachina/backend/.env')
load_dotenv(dotenv_path=env_path)

from personality import RoasterEngine
app = FastAPI(title="The Roast Office")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = RoasterEngine()
ACTIVE_THREAD = {"id": None}

@app.on_event("startup")
async def startup_event():
    try:
        thread_obj = await engine.client.create_thread(engine.assistant_id)
        ACTIVE_THREAD["id"] = thread_obj.thread_id
        print(f"🚀 Roaster Thread Active: {ACTIVE_THREAD['id']}")
    except Exception as e:
        print(f"⚠️ Startup thread warning: {e}")

@app.post("/roast")
async def roast_text(
    background_tasks: BackgroundTasks,
    text: str = Body(...), 
    tier: str = Body("medium"), 
    style: str = Body("tech_bro")
):
   
    background_tasks.add_task(engine.save_excuse_to_memory, text, style)

    persona = engine.get_roast_persona(tier, style)
    api_key = os.getenv("BACKBOARD_API_KEY", "").strip()
    
    
    headers = {
        "X-API-Key": api_key,
        "authorization": f"Bearer {api_key}", 
        "Content-Type": "application/json"
    }
    
    
    chat_url = "https://app.backboard.io/api/threads/messages"
    chat_payload = {
        "thread_id": str(ACTIVE_THREAD["id"]), 
        "assistant_id": engine.assistant_id,
        "content": f"SYSTEM INSTRUCTION: {persona}\n\nUSER REPLY: {text}",
        "llm_provider": "openai", 
        "model_name": "gpt-4o",
        "stream": False,
        "send_to_llm": "true", 
        "memory": "on", 
        "web_search": "off"
    }

    async with httpx.AsyncClient() as client:
        try:
            
            chat_res = await client.post(chat_url, headers=headers, json=chat_payload, timeout=30.0)
            chat_data = chat_res.json()
            roast_content = chat_data.get("content", "Nonsense.")

            voice_map = {
                "nigeria_parent": "en-NG-Standard-A",
                "tech_bro": "en-US-Neural2-D",
                "bitter_ex": "en-GB-Neural2-B",
                "passive_aggressive_coworker": "en-IE-Standard-A"
            }
            
            speech_url = "https://app.backboard.io/api/tts"
            speech_payload = {
                "text": roast_content,
                "voice": voice_map.get(style, "en-US-Neural2-F"),
                "speed": 1.0
            }
            
            speech_res = await client.post(speech_url, headers=headers, json=speech_payload)
            speech_data = speech_res.json()
            
            
            print(f"DEBUG: Speech API Response: {speech_data}") 
            
            audio_url = speech_data.get("audio_url") or speech_data.get("url")

            return {
                "roast": roast_content,
                "audio_url": audio_url,
                "metadata": {"tier": tier, "style": style}
            }
            
        except Exception as e:
            print(f" Backend Error: {e}")
            return {"error": "Connection Failed", "details": str(e)}