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
        <h1 id="text">FOR<br></br>ALL GAMERS</h1>
      </div>
    </>
  )
}

export default page

