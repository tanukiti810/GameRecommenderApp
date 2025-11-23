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
              borderColor: '#135389',
              color: '#135389',
              borderWidth: 3,
              fontSize: '0.9rem',
              padding: '14px 36px',
            }
          }}>
          <Button variant="outlined" onClick={() => sendData("Action")}>アクション</Button>
          <Button variant="outlined" onClick={() => sendData("Adventure")}>アドベンチャー</Button>
          <Button variant="outlined" onClick={() => sendData("RPG")}>RPG</Button>
          <Button variant="outlined" onClick={() => sendData("")}>シューティング</Button>
          <Button variant="outlined" onClick={() => sendData("ジャンル5")}>アクションアドベンチャー</Button>
          <Button variant="outlined" onClick={() => sendData("ジャンル6")}>シミュレーション</Button>
          <Button variant="outlined" onClick={() => sendData("ジャンル6")}>サンドボックス</Button>
          <Button variant="outlined" onClick={() => sendData("ジャンル6")}>ストラテジー</Button>
          <Button variant="outlined" onClick={() => sendData("ジャンル6")}>タクティクス</Button>
          <Button variant="outlined" onClick={() => sendData("ジャンル6")}>スポーツ</Button>
          <Button variant="outlined" onClick={() => sendData("ジャンル6")}>レース</Button>
          <Button variant="outlined" onClick={() => sendData("ジャンル6")}>カジュアル</Button>
          <Button variant="outlined" onClick={() => sendData("ジャンル6")}>ホラー</Button>
          <Button variant="outlined" onClick={() => sendData("ジャンル6")}>サスペンス</Button>
          <Button variant="outlined" onClick={() => sendData("ジャンル6")}>インディー</Button>
        </Box>
      </div>
    </>

  )
}

export default ChoosePage