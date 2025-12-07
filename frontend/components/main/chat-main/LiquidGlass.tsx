import React, { useState } from "react";
import SendIcon from "@mui/icons-material/Send";

interface ChatInputProps {
    onSend: (message: string) => void;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSend }) => {
    const [message, setMessage] = useState("");

    const handleSend = () => {
        if (!message.trim()) return;
        onSend(message);
        setMessage("");
    };

    return (
            <div className="liquid-glass-card">
                <input
                    className='liquid-glass-button'
                    type="text"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleSend()}
                    placeholder="Type your message..."
                />
                <button className="liquid-glass-button" onClick={handleSend}><SendIcon /></button>
            </div>
    );
};

export default ChatInput;
