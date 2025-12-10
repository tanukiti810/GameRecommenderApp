'use client';

import Button from '@mui/material/Button';
import { useRouter } from 'next/navigation';

const GameSelect = () => {
  const router = useRouter();

  return (
    <>
      <div style={{
        height: '100vh',
        boxSizing: 'border-box',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center'
      }}>
        <div className='select-header'>
          <div>select components</div>
        </div>

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
      </div>
    </>
  );
};

export default GameSelect;
