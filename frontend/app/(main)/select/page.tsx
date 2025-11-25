'use client';

import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import { useRouter } from 'next/navigation';

const GameSelect = () => {
  const router = useRouter();

  return (
    <>
      <div style={{
        height: '100vh', 
        boxSizing: 'border-box'
      }}>
        <div className='select-header'>
          <div>select components</div>
        </div>

        <Box
          sx={{
            '& button': {
              m: 2,
              borderColor: '#135389',
              color: '#135389',
              borderWidth: 3,
              fontSize: '0.9rem',
              padding: '14px 36px',
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
      </div>
    </>
  );
};

export default GameSelect;
