import { useEffect, useRef } from 'react';
import MessageItem from './MessageItem';

interface Message {
    id: string;
    text: string;
    sender: "user" | "ai";
}

interface ChatWindowProps {
    messages: Message[];
    isLoading?: boolean;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ messages,isLoading }) => {
    const chatEndRef = useRef<HTMLDivElement>(null)

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);
    return (
        <div className="chat-window">
            <div className='chatElement'>
                {/* 配列messagesを順番に表示 */}
                {messages.map(msg => (
                    <MessageItem key={msg.id} text={msg.text} sender={msg.sender} />
                ))}
                {isLoading && (
                    <MessageItem
                        text="..."
                        sender="ai"
                    />
                )}
                <div ref={chatEndRef} />
            </div>
        </div>
    );
};

export default ChatWindow;
