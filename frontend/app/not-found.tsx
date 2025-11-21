import React from 'react';
import Link from 'next/link';

export default function NotFound() {
  return (
    <div style={{
      height: '100vh',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      textAlign: 'center',
      padding: '20px'
    }}>
      <h1>404 - Page Not Found</h1>
      <p>お探しのページは見つかりませんでした。</p>

      <Link href="/">
        <button style={{
          marginTop: '20px',
          padding: '10px 20px',
          border: '2px solid #000',
          background: 'transparent',
          cursor: 'pointer'
        }}>
          Go Back Home
        </button>
      </Link>
    </div>
  );
}
