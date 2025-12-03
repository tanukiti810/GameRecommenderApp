'use client';

import { Button, TextField } from '@mui/material';

export default function ChatPage() {
  return (
    <div>
      <h1>ChatAI</h1>
      <TextField type="text" placeholder="Type your message..." />
      <Button variant="outlined">Send</Button>
    </div>
  );
}
