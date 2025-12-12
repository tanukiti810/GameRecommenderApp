"use client";
import { useState } from "react";
import ChatWindow from "../../../../components/main/chat-main/ChatWindow";
import ChatInput from "../../../../components/main/chat-main/ChatInput";

type Sender = "user" | "ai";

interface Message {
  id: string;
  text: string;
  sender: Sender;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
  {
    id: "welcome-ai",
    text: "ゲームの事なら何でも聞いて！何か質問ある？",
    sender: "ai",
  },
]);

  const handleSend = async (text: string) => {
    const trimmed = text.trim();
    if (!trimmed) return;

 

    const userMsg: Message = {
      id: crypto.randomUUID(),
      text: trimmed,
      sender: "user",
    };
    setMessages((prev) => [...prev, userMsg]);

    try {

      const historyForApi = [...messages, userMsg].map((m) => ({
        role: m.sender === "user" ? "user" : "assistant",
        content: m.text,
      }));


      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: trimmed,
          history: historyForApi,
        }),
      });

      if (!res.ok) {
        const errText = await res.text();
        console.error("chat api error", res.status, errText);
        const errorMsg: Message = {
          id: crypto.randomUUID(),
          text: "ごめん、サーバー側でエラー出てるっぽい…🙏",
          sender: "ai",
        };
        setMessages((prev) => [...prev, errorMsg]);
        return;
      }

      const data: { reply: string } = await res.json();

      const aiMsg: Message = {
        id: crypto.randomUUID(),
        text: data.reply,
        sender: "ai",
      };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (e) {
      console.error(e);
      const errorMsg: Message = {
        id: crypto.randomUUID(),
        text: "ネットワークエラーっぽい…もう一回送ってみて！",
        sender: "ai",
      };
      setMessages((prev) => [...prev, errorMsg]);
    }
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
