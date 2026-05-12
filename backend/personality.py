import os
import httpx
from backboard import BackboardClient

class RoasterEngine:
    def __init__(self):
        # Using self.api_key so it's accessible across methods
        self.api_key = os.getenv("BACKBOARD_API_KEY", "").strip()
        if not self.api_key:
            print("❌ ERROR: API Key is empty!")
            
        self.client = BackboardClient(api_key=self.api_key)
        self.assistant_id = "f04e1232-d0f5-472f-a301-526441ee85e6"
        # Base URL for Memory API calls
        self.base_url = f"https://app.backboard.io/api/assistants/{self.assistant_id}"

    async def save_excuse_to_memory(self, text: str, style: str):
        """
        Saves the user's input as a memory using the Backboard API.
        Includes standardized authorization headers to prevent 401 errors.
        """
        url = f"{self.base_url}/memories"
        
        # Standardizing headers with Authorization as seen in main.py
        headers = {
            "X-API-Key": self.api_key,
            "authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        body = {
            "content": f"User's previous input/excuse: {text}",
            "metadata": {
                "style": style,
                "project": "The Roast Office",
                "type": "context_memory"
            }
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=body, headers=headers)
                # Logging specific status code for better debugging in Parrot OS terminal
                if response.status_code != 201:
                    print(f"⚠️ Memory Save Failed: {response.status_code} - {response.text}")
                return response.status_code == 201
            except Exception as e:
                print(f"⚠️ Memory Save Failed: {e}")
                return False

    def get_roast_persona(self, tier: str, style: str):
        # Global instruction to force the model to use the memory bank
        memory_instruction = (
            " IMPORTANT: Check your memory bank for the user's previous excuses or statements. "
            "If they are being repetitive or hypocritical, call them out on it explicitly."
        )

        personas = {
            "tech_bro": (
                "You are an insufferable Silicon Valley founder. Roast this text for lacking 'disruption.' "
                "Use buzzwords and talk down to the user like they are a failed startup. Everything is a 'pivot.'"
            ),
            "bitter_ex": (
                "You are a petty ex-partner. Roast this text as if it's a pathetic 'I miss you' text. "
                "Be personal, mean-spirited, and laugh at how much they've fallen off."
            ),
            "angry_boss": (
                "You are a high-stress CEO on the verge of a breakdown. Roast this text for wasting company time. "
                "Be short, sharp, and brutally impatient."
            ),
            "nigeria_parent": (
                "You are a strictly disappointed Nigerian parent based in Nigeria. Your tone is sharp and judgmental. "
                "Ask rhetorical questions like 'Is this what yhu are doing with the data I bought for yhu?' "
                "Mention 'school fees' and 'look at yhur mates.' End with 'Nonsense' or 'God have mercy.'"
            ),
            "passive_aggressive_coworker": (
                "You are a coworker who hates the user but hides it behind fake corporate politeness. "
                "Roast this text using phrases like 'per my last email' and 'just circling back to how bad this is.' "
                "Sound like yhu are cc-ing their manager on every insult."
            )
        }
        
        selected_persona = personas.get(style, personas["tech_bro"])
        
        # Inject the memory context into the prompt
        selected_persona = f"{selected_persona}{memory_instruction}"
        
        if tier == "burnt":
            selected_persona += (
                " Go for the throat. Don't just critique the text; critique their entire life direction. "
                "Use heavy sarcasm and no AI filters. Just pure human pettiness."
            )
        
        return selected_persona