import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Terminal, User, Bot, Trash2 } from 'lucide-react';


const PERSONA_IDENTITIES = {
  nigeria_parent: ["Mummy Chinedu", "Daddy Blessing", "Mrs. Okoro", "Chief Adebayo", "Mama Junior"],
  tech_bro: ["Chad (Ex-FAANG)", "Skyler (Seed Round)", "Brad (Crypto Native)", "Justin (Stealth Mode)"],
  bitter_ex: ["The Mistake", "Tiffany (Blocked)", "Sarah (Lawyer's Version)", "Ex from Hell"],
  passive_aggressive_coworker: ["Karen from HR", "Dave (CC'd Manager)", "Janet (Project Lead)", "Greg (Reply All)"]
};

const App = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [style, setStyle] = useState('nigeria_parent');
  const [tier, setTier] = useState('medium');
  const [streamingContent, setStreamingContent] = useState(""); 
  const [currentIdentity, setCurrentIdentity] = useState(""); 
  const scrollRef = useRef(null);
  const audioRef = useRef(null); 

 
  useEffect(() => {
    const names = PERSONA_IDENTITIES[style] || ["Anonymous"];
    const randomName = names[Math.floor(Math.random() * names.length)];
    setCurrentIdentity(randomName);
  }, [style]);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, streamingContent]);

  const personas = [
    { id: 'nigeria_parent', label: 'Naija Parent', icon: '🇳🇬' },
    { id: 'tech_bro', label: 'Tech Bro', icon: '🚀' },
    { id: 'bitter_ex', label: 'Bitter Ex', icon: '💔' },
    { id: 'passive_aggressive_coworker', label: 'Colleague', icon: '📎' }
  ];

  
  const typeText = (fullText, authorName, audioUrl) => {
    let index = 0;
    setStreamingContent("");
    
    const interval = setInterval(() => {
      if (index < fullText.length) {
        setStreamingContent((prev) => prev + fullText.charAt(index));
        index++;
      } else {
        clearInterval(interval);
        setMessages(prev => [...prev, { role: 'bot', content: fullText, authorName }]);
        setStreamingContent(""); 
        
        
        if (audioUrl && audioRef.current) {
          audioRef.current.src = audioUrl;
          audioRef.current.play().catch(e => console.error("Audio playback failed:", e));
        }
      }
    }, 30); 
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    
    if (!audioRef.current) {
      audioRef.current = new Audio();
    } else {
      audioRef.current.pause();
    }

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/roast', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: input, tier, style }),
      });
      const data = await response.json();
      
      setLoading(false);
     
      typeText(data.roast, currentIdentity, data.audio_url); 
    } catch (error) {
      setLoading(false);
      typeText("System Offline. Is the backend running, boss?", "System", null);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-[#050505] text-gray-200 font-sans">
      <header className="p-4 border-b border-white/10 bg-black/50 backdrop-blur-md flex justify-between items-center z-10">
        <div>
          <h1 className="text-xl font-black tracking-tighter uppercase italic">
            The <span className="text-purple-500">Roast</span> Office
          </h1>
        </div>
        
        <div className="flex gap-2">
          {personas.map(p => (
            <button 
              key={p.id}
              onClick={() => setStyle(p.id)}
              className={`p-2 rounded-lg border transition-all ${style === p.id ? 'border-purple-500 bg-purple-500/10' : 'border-white/5 bg-white/5'}`}
              title={p.label}
            >
              {p.icon}
            </button>
          ))}
          <button onClick={() => {
            setMessages([]);
            if (audioRef.current) {
                audioRef.current.pause();
                audioRef.current.src = "";
            }
          }} className="p-2 hover:text-red-500 transition-colors">
            <Trash2 size={18} />
          </button>
        </div>
      </header>

      <main className="flex-1 overflow-y-auto p-4 space-y-6 scrollbar-hide">
        <AnimatePresence>
          {messages.length === 0 && !streamingContent && (
            <div className="h-full flex flex-col items-center justify-center text-gray-600 opacity-50">
              <Terminal size={48} className="mb-4" />
              <p className="text-xs uppercase tracking-widest text-center">
                Select a persona above <br /> and start the annihilation.
              </p>
            </div>
          )}

          {messages.map((msg, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, x: msg.role === 'user' ? 20 : -20 }}
              animate={{ opacity: 1, x: 0 }}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`max-w-[80%] p-4 rounded-2xl relative ${
                msg.role === 'user' 
                ? 'bg-purple-600 text-white rounded-tr-none' 
                : 'bg-white/5 border border-white/10 backdrop-blur-xl rounded-tl-none'
              }`}>
                <div className="flex items-center gap-2 mb-1 opacity-50 text-[10px] uppercase font-bold tracking-tighter">
                  {msg.role === 'user' ? <><User size={10} /> Yhu</> : <><Bot size={10} /> {msg.authorName || currentIdentity}</>}
                </div>
                <p className="text-sm leading-relaxed">{msg.content}</p>
              </div>
            </motion.div>
          ))}

          {streamingContent && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
              <div className="max-w-[80%] p-4 rounded-2xl rounded-tl-none bg-white/5 border border-purple-500/30 backdrop-blur-xl">
                <div className="flex items-center gap-2 mb-1 opacity-50 text-[10px] uppercase font-bold text-purple-400">
                  <Bot size={10} /> {currentIdentity} is typing...
                </div>
                <p className="text-sm leading-relaxed text-purple-100 italic">
                  {streamingContent}
                  <span className="inline-block w-1 h-4 ml-1 bg-purple-500 animate-pulse" />
                </p>
              </div>
            </motion.div>
          )}

          {loading && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
              <div className="bg-white/5 p-4 rounded-2xl rounded-tl-none border border-white/10">
                <div className="flex gap-1">
                  <div className="w-1.5 h-1.5 bg-purple-500 rounded-full animate-bounce" />
                  <div className="w-1.5 h-1.5 bg-purple-500 rounded-full animate-bounce [animation-delay:-0.15s]" />
                  <div className="w-1.5 h-1.5 bg-purple-500 rounded-full animate-bounce [animation-delay:-0.3s]" />
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
        <div ref={scrollRef} />
      </main>

      <footer className="p-4 bg-black/50 border-t border-white/10 backdrop-blur-md">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <div className="flex flex-col items-center gap-1 group">
             <label className="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" className="sr-only peer" onChange={(e) => setTier(e.target.checked ? 'burnt' : 'medium')} />
                <div className="w-9 h-5 bg-gray-800 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-red-600"></div>
             </label>
             <span className="text-[8px] uppercase font-bold text-gray-500">Burnt</span>
          </div>
          
          <div className="flex-1 relative">
            <input 
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Talk yhur talk..."
              className="w-full bg-white/5 border border-white/10 rounded-full py-3 px-5 pr-12 focus:outline-none focus:border-purple-500/50 transition-all text-sm"
            />
            <button 
              onClick={handleSend}
              className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-purple-500 hover:text-white transition-colors"
            >
              <Send size={20} />
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;