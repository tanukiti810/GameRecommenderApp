'use client';

import { Button } from '@mui/material'
import React from 'react'
import '../../App.css'



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
      <div> ChooseGamediv</div>
      <div className='ChooseBox select_Genre'>
        <Button variant="outlined" onClick={() => sendData("ジャンル1")}>ジャンル１</Button>
        <Button variant="outlined" onClick={() => sendData("ジャンル2")}>ジャンル２</Button>
        <Button variant="outlined" onClick={() => sendData("ジャンル3")}>ジャンル３</Button>
        <Button variant="outlined" onClick={() => sendData("ジャンル4")}>ジャンル４</Button>
        <Button variant="outlined" onClick={() => sendData("ジャンル5")}>ジャンル５</Button>
        <Button variant="outlined" onClick={() => sendData("ジャンル6")}>ジャンル６</Button>
      </div>
      <div className='ChooseBox select_Type'>
        <Button variant="outlined" onClick={() => sendData("タイプ1")}>タイプ１</Button>
        <Button variant="outlined" onClick={() => sendData("タイプ2")}>タイプ２</Button>
        <Button variant="outlined" onClick={() => sendData("タイプ2")}>タイプ３</Button>
        <Button variant="outlined" onClick={() => sendData("タイプ3")}>タイプ４</Button>
        <Button variant="outlined" onClick={() => sendData("タイプ4")}>タイプ５</Button>
        <Button variant="outlined" onClick={() => sendData("タイプ5")}>タイプ６</Button>
      </div>
    </>

  )
}

export default ChoosePage