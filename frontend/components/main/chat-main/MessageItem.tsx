const MessageItem = ({ text, sender }: { text: string; sender: "user" | "ai" }) => {
  return (
    <div className={`message-item ${sender}`}>
      {text}
    </div>
  );
};
export default MessageItem;
