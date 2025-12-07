"use client";
import { useState } from "react";
import ChatWindow from "../../../../components/main/chat-main/ChatWindow";
import ChatInput from "../../../../components/main/chat-main/ChatInput";


export default function ChatPage() {
  const [messages, setMessages] = useState<{ id: string; text: string; sender: "user" | "ai" }[]>([]);

  const handleSend = (text: string) => {
    const userMsg = {
      id: crypto.randomUUID(),
      text,
      sender: "user" as const
    };
    setMessages(prev => [...prev, userMsg]);
    //ここでAIの返答を設定
    const aiMsg = {
      id: crypto.randomUUID(),
      text: "AIの返信です",
      sender: "ai" as const
    };

    setTimeout(() => setMessages(prev => [...prev, aiMsg]), 500);
  };



  return (
    <div className="background">
      <div className="chatPage">
        <ChatWindow messages={messages} />
        <ChatInput onSend={handleSend} />
      </div>
    </div>
  );
}

