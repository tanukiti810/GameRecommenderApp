'use client';

import { Box, Button } from '@mui/material'
import React from 'react'
import '../../../App.css'
import '../../../globals.css'
import SidebarSelect from '@/components/main/select-main/SidebarSelect';

const ChoosePage = () => {


  const sendData = async (value: string) => {
    await fetch("http://localhost:8000/api/choose", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ selected: value })
    });
  }


  return (
    <>
      <div className='choosePage flex'>
        <SidebarSelect />
        <div className='ChooseBox select_Genre'>
        </div>
      </div>
    </>

  )
}

export default ChoosePage