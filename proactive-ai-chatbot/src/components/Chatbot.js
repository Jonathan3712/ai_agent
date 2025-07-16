import React, { useState } from 'react';

function Chatbot() {
  const [messages, setMessages] = useState([]); // { sender: 'user' | 'bot' | 'proactive' | 'error', text: '' }
  const [input, setInput] = useState('');

  const handleSend = async () => {
    if (!input.trim()) return;

    // Add user message to chat
    setMessages(prev => [...prev, { sender: 'user', text: input }]);

    try {
      // Call backend API
      const res = await fetch('https://proactive-ai-agent.onrender.com/api/events', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          last_user_message: input,
          inactivity_seconds: 0
        })
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data = await res.json();

      // Add bot reply
      setMessages(prev => [
        ...prev,
        { sender: 'bot', text: data.bot_reply }
      ]);

      // Add proactive message if any
      if (data.proactive_message) {
        setMessages(prev => [
          ...prev,
          { sender: 'proactive', text: data.proactive_message }
        ]);
      }

      // Clear input box
      setInput('');
    } catch (err) {
      console.error('Error connecting to backend:', err);
      setMessages(prev => [...prev, { sender: 'error', text: 'Error connecting to server' }]);
    }
  };

  return (
    <div style={{ width: 400, margin: 'auto', fontFamily: 'Arial, sans-serif' }}>
      <h3>Proactive AI Chatbot</h3>
      <div
        style={{
          border: '1px solid #ccc',
          height: 300,
          overflowY: 'auto',
          padding: 10,
          marginBottom: 10,
          backgroundColor: '#f9f9f9'
        }}
      >
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              textAlign: msg.sender === 'user' ? 'right' : 'left',
              marginBottom: 8,
              color:
                msg.sender === 'user'
                  ? '#007bff'
                  : msg.sender === 'bot'
                  ? '#000'
                  : msg.sender === 'proactive'
                  ? '#28a745'
                  : '#dc3545'
            }}
          >
            <strong>{msg.sender}:</strong> {msg.text}
          </div>
        ))}
      </div>
      <input
        value={input}
        onChange={e => setInput(e.target.value)}
        style={{ width: '80%', padding: 8, fontSize: 14 }}
        placeholder="Type your message..."
        onKeyDown={e => {
          if (e.key === 'Enter') {
            handleSend();
          }
        }}
      />
      <button onClick={handleSend} style={{ padding: '8px 16px', marginLeft: 8 }}>
        Send
      </button>
    </div>
  );
}

export default Chatbot;
