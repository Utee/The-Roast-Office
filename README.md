
```markdown
# 🔥 The Roast Office

A high-fidelity "disappointment-as-a-service" platform built for the **Backboard Hackathon**. The Roast Office uses AI to annihilate your excuses with the biting wit of unique personas, from strictly disappointed Nigerian parents to insufferable tech bros.

## 🛠️ Tech Stack
- **Frontend:** React + Vite, Framer Motion (for smooth terminal vibes), Lucide Icons.
- **Backend:** FastAPI (Python), HTTPX for asynchronous API calls.
- **AI Engine:** Backboard API for personality-driven memory and roast generation.
- **OS:** Developed and optimized on **Parrot OS**.

## ✨ Features
- **Persona-Based Roasting:** Switch between "Naija Parent," "Tech Bro," "Bitter Ex," or "Passive-Aggressive Colleague".
- **Contextual Memory:** Utilizing Backboard's Memory API, the system remembers your previous inputs to call out inconsistency and hypocrisy.
- **Typewriter Streaming:** Real-time text animation for a vintage terminal aesthetic.
- **Voice Synthesis:** Integrated browser-based Speech API to deliver roasts with localized pitch and speed.

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js & npm

### Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/Utee/The-Roast-Office.git](https://github.com/Utee/The-Roast-Office.git)
   cd The-Roast-Office

```

2. **Backend Configuration**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn httpx python-dotenv backboard-sdk

```


*Create a `.env` file in the `backend` directory with your API keys:*
```env
BACKBOARD_API_KEY=your_key_here

```


3. **Frontend Configuration**
```bash
cd ../frontend
npm install
npm run dev

```



## 📂 Project Structure

* `App.jsx`: Main interface logic, typewriter effect, and browser TTS integration.
* `main.py`: FastAPI routes, thread management, and API orchestration.
* `personality.py`: Logic for memory persistence and persona prompt engineering.
* `.gitignore`: Configured to protect sensitive `.env` files and ignore bulky dependencies.

---

*Created by Utibe-Abasi Jacob Udoh for the Backboard Hackathon 2026*

