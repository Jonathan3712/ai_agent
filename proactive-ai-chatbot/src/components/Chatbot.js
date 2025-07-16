import React, { useState } from 'react';

function Chatbot() {
  const [messages, setMessages] = useState([]); // { sender: 'user' | 'bot' | 'proactive', text: '' }
  const [input, setInput] = useState('');

  const handleSend = async () => {
    if (!input.trim()) return;

    // Add user message
    setMessages(prev => [...prev, { sender: 'user', text: input }]);

    try {
      // Send to backend
      const res = await fetch('https://<YOUR-RENDER-URL>/api/events', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          last_user_message: input,
          inactivity_seconds: 0
        })
      });
      const data = await res.json();

      // Add bot reply
      setMessages(prev => [...prev,
        { sender: 'user', text: input },
        { sender: 'bot', text: data.bot_reply }
      ]);

      // If proactive message exists
      if (data.proactive_message) {
        setMessages(prev => [...prev,
          { sender: 'bot', text: data.bot_reply },
          { sender: 'proactive', text: data.proactive_message }
        ]);
      }

      setInput('');
    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, { sender: 'error', text: 'Error connecting to server' }]);
    }
  };

  return (
    <div style={{ width: '400px', margin: 'auto' }}>
      <h3>Proactive AI Chatbot</h3>
      <div style={{ border: '1px solid #ccc', height: '300px', overflowY: 'scroll', padding: '10px' }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ textAlign: msg.sender === 'user' ? 'right' : 'left' }}>
            <strong>{msg.sender}:</strong> {msg.text}
          </div>
        ))}
      </div>
      <input
        value={input}
        onChange={e => setInput(e.target.value)}
        style={{ width: '80%' }}
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}

export default Chatbot;
