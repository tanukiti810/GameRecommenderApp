'use client';

import React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import '../App.css';
import { useRouter } from 'next/navigation';

const GameSelect = () => {
  const router = useRouter();

  return (
    <>
      <div>Select pageaaaa</div>

      <Box
        sx={{
          '& button': {
            m: 2,
            borderWidth: 3,
            fontSize: '0.9rem',
            padding: '14px 36px',
            width: '300px',
            height: '100px'
          }
        }}
      >
        <div className="ButtonBox">
          <div className="BoxContainer">
            {/* Chat ページへ */}
            <Button
              variant="outlined"
              className="largeButton"
              onClick={() => router.push('/select/chat')}
            >
              Wanna Find Out??
              <br />
              Let's Chat!!
            </Button>

            {/* Choose ページへ */}
            <Button
              variant="outlined"
              className="largeButton"
              onClick={() => router.push('/select/choose')}
            >
              wanna choose questions
              <br />
              your like??
            </Button>
          </div>
        </div>
      </Box>
    </>
  );
};

export default GameSelect;
