import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface MessageResponse {
  message: string;
}

const App: React.FC = () => {
  const [message, setMessage] = useState<string>("");

  useEffect(() => {
    axios.get<MessageResponse>('http://localhost:8000/')
      .then(response => {
        setMessage(response.data.message);
      })
      .catch(error => {
        console.error("Error fetching data:", error);
      });
  }, []);

  return (
    <div>
      <h1>TypeScript + FastAPI, github変更加えました</h1>
      <p>{message}</p>
    </div>
  );
};

export default App;
