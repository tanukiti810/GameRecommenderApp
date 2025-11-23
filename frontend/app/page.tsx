'use client'

import React, { useState } from 'react'
import './globals.css'
import Particles from "../components/main/Particles";
import { Button } from '@mui/material';
import { useRouter } from 'next/navigation';

const page = () => {
  const router = useRouter();
  return (
    <>
      <div className="text">
        <h1 id="text">キャッチ<br></br>フレーズ</h1>
      </div>
      <div>
        <Button variant="outlined" onClick={() => router.push('/select')}>button</Button>
      </div>
    </>
  )
}

export default page

