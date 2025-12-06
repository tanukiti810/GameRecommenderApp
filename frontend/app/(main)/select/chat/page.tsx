"use client";
import { useState } from "react";
import ChatWindow from "../../../../components/main/chat-main/ChatWindow";
import LiquidGlass from "../../../../components/main/chat-main/LiquidGlass";


export default function ChatPage() {
  const [messages, setMessages] = useState<{ id: string; text: string; sender: "user" | "ai" }[]>([]);


  const handleSend = (text: string) => {
    const userMsg = { id: Date.now().toString(), text, sender: "user" as const };
    setMessages(prev => [...prev, userMsg]);
    const aiMsg = {
      id: (Date.now() + 1).toString(),
      text: "AIの返信です",
      sender: "ai" as const
    };

    setTimeout(() => setMessages(prev => [...prev, aiMsg]), 500);
  };


  return (
    <div className="chat-page-wrapper">
      <div className="background">
        <ChatWindow messages={messages} />
        <LiquidGlass onSend={handleSend} />
      </div>
    </div>
  );
}

