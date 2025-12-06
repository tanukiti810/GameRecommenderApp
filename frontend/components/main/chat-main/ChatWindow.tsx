interface Message {
  id: string;
  text: string;
  sender: "user" | "ai";
}

interface ChatWindowProps {
  messages: Message[];
}

const ChatWindow: React.FC<ChatWindowProps> = ({ messages }) => {
  return (
    <div className="chat-window">
      {messages.map(msg => (
        <div
          key={msg.id}
          className={`message-item ${msg.sender === "user" ? "user" : "ai"}`}
        >
          {msg.text}
        </div>
      ))}
    </div>
  );
};

export default ChatWindow;
