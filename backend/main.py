import os
import httpx
import subprocess  
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
        print(f" Roaster Thread Active: {ACTIVE_THREAD['id']}")
    except Exception as e:
        print(f" Startup thread warning: {e}")

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
    
    voice_map = {
        "nigeria_parent": "onyx",
        "tech_bro": "fable",
        "bitter_ex": "shimmer",
        "passive_aggressive_coworker": "nova"
    }
    selected_voice = voice_map.get(style, "alloy")

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
        "web_search": "off",
        "voice": {
            "tts": {
                "provider": "openai",
                "model": "gpt-4o-mini-tts",
                "voice": selected_voice
            }
        }
    }

    async with httpx.AsyncClient() as client:
        try:
            chat_res = await client.post(chat_url, headers=headers, json=chat_payload, timeout=30.0)
            chat_data = chat_res.json()
            roast_content = chat_data.get("content", "Nonsense.")

            audio_url = None
            messages_list = chat_data.get("messages", [])
            if messages_list:
                audio_url = messages_list[-1].get("voice_records", {}).get("tts", {}).get("audio_url")
            else:
                audio_url = chat_data.get("voice_records", {}).get("tts", {}).get("audio_url")

            print(f"DEBUG: Text Roast: {roast_content[:50]}...")
            print(f"DEBUG: Generated Audio URL: {audio_url}")
            try:
                
                speed = "140" if style == "nigeria_parent" else "175"
                pitch = "40" if style == "nigeria_parent" else "70"
                
                subprocess.Popen(["espeak", "-s", speed, "-p", pitch, roast_content])
            except Exception as audio_err:
                print(f"⚠️ Local audio playback skip: {audio_err}")
           

            return {
                "roast": roast_content,
                "audio_url": audio_url,
                "metadata": {"tier": tier, "style": style}
            }
            
        except Exception as e:
            print(f" Backend Error: {e}")
            return {"error": "Connection Failed", "details": str(e)}