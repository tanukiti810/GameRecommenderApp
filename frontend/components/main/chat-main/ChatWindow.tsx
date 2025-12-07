import { useEffect, useRef } from 'react';
import MessageItem from './MessageItem';

interface Message {
    id: string;
    text: string;
    sender: "user" | "ai";
}

interface ChatWindowProps {
    messages: Message[];
}

const ChatWindow: React.FC<ChatWindowProps> = ({ messages }) => {
    const chatEndRef = useRef<HTMLDivElement>(null)

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);
    return (
        <div className="chat-window">
            <div className='chatElement'>
                {messages.map(msg => (
                    <MessageItem key={msg.id} text={msg.text} sender={msg.sender} />
                ))}
                <div ref={chatEndRef} />
            </div>
        </div>
    );
};

export default ChatWindow;
