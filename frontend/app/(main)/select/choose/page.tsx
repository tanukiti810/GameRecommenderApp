'use client';

import { Box, Button } from '@mui/material'
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
        <Box
          sx={{
            '& button': {
              m: 2,
              borderColor: '#344699',
              color: '#344699',
              borderWidth: 3,
              fontSize: '0.9rem',
              padding: '14px 36px',
            }
          }}>
          <Button variant="outlined" onClick={() => sendData("Action")}>アクション</Button>
          <Button variant="outlined" onClick={() => sendData("Adventure")}>アドベンチャー</Button>
          <Button variant="outlined" onClick={() => sendData("RPG")}>RPG</Button>
          <Button variant="outlined" onClick={() => sendData("Shooting")}>シューティング</Button>
          <Button variant="outlined" onClick={() => sendData("ActionAdventure")}>アクションアドベンチャー</Button>
          <Button variant="outlined" onClick={() => sendData("Simulation")}>シミュレーション</Button>
          <Button variant="outlined" onClick={() => sendData("SandBox")}>サンドボックス</Button>
          <Button variant="outlined" onClick={() => sendData("Strategy")}>ストラテジー</Button>
          <Button variant="outlined" onClick={() => sendData("Tactics")}>タクティクス</Button>
          <Button variant="outlined" onClick={() => sendData("Sports")}>スポーツ</Button>
          <Button variant="outlined" onClick={() => sendData("Racing")}>レース</Button>
          <Button variant="outlined" onClick={() => sendData("Casual")}>カジュアル</Button>
          <Button variant="outlined" onClick={() => sendData("Horror")}>ホラー</Button>
          <Button variant="outlined" onClick={() => sendData("Suspense")}>サスペンス</Button>
          <Button variant="outlined" onClick={() => sendData("Indy")}>インディー</Button>
        </Box>
      </div>
    </>

  )
}

export default ChoosePage