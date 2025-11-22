'use client';

import { Button } from '@mui/material'
import React from 'react'
import '../../../App.css'



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
      <div>Choose</div>
      <div className='ChooseBox select_Genre'>
        <Button variant="outlined" onClick={() => sendData("Action")}>アクション</Button>
        <Button variant="outlined" onClick={() => sendData("Adventure")}>アドベンチャー</Button>
        <Button variant="outlined" onClick={() => sendData("RPG")}>RPG</Button>
        <Button variant="outlined" onClick={() => sendData("ジャンル4")}>ジャンル４</Button>
        <Button variant="outlined" onClick={() => sendData("ジャンル5")}>ジャンル５</Button>
        <Button variant="outlined" onClick={() => sendData("ジャンル6")}>ジャンル６</Button>
      </div>
      <div className='ChooseBox select_Type'>
        <Button variant="outlined" onClick={() => sendData("Single-player")}>シングルプレイヤー</Button>
        <Button variant="outlined" onClick={() => sendData("Multi-player")}>マルチプレイヤー</Button>
        <Button variant="outlined" onClick={() => sendData("")}>タイプ３</Button>
        <Button variant="outlined" onClick={() => sendData("タイプ3")}>タイプ４</Button>
        <Button variant="outlined" onClick={() => sendData("タイプ4")}>タイプ５</Button>
        <Button variant="outlined" onClick={() => sendData("タイプ5")}>タイプ６</Button>
      </div>
    </>

  )
}

export default ChoosePage