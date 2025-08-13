import logo from './logo.svg';
import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;

import React, { useState } from 'react';

function App() {
  const [message, setMessage] = useState('');
  const [chatLog, setChatLog] = useState([]);

  const sendMessage = async () => {
    if (!message.trim()) return;
  
    // Add user's message to chat
    const newLog = [...chatLog, { sender: 'You', text: message }];
    setChatLog(newLog);
  
    try {
      const res = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });
  
      const data = await res.json();
  
      // Append Q's response to chat
      setChatLog([...newLog, { sender: 'You', text: message }, { sender: 'Q', text: data.reply }]);
    } catch (error) {
      console.error('Error fetching from backend:', error);
      setChatLog([...newLog, { sender: 'Q', text: 'Error: Could not reach backend.' }]);
    }
  
    setMessage('');
  };
  

  return (
    <div style={{ padding: 20 }}>
      <h2>Amazon Q Chatbot</h2>
      <div style={{ border: '1px solid #ccc', padding: 10, height: 300, overflowY: 'scroll' }}>
        {chatLog.map((msg, index) => (
          <div key={index}><strong>{msg.sender}:</strong> {msg.text}</div>
        ))}
      </div>
      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        style={{ width: '80%', marginTop: 10 }}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default App;
