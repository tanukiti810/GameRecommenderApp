'use client';

import { Card, CardActions, CardContent, Typography } from '@mui/material';
import Button from '@mui/material/Button';
import { useRouter } from 'next/navigation';

const cardStyle = {
  width: 400,
  height: 520,               // 固定高さに変更
  display: "flex",
  flexDirection: "column",
  justifyContent: "space-between",
};

const textCenter = { textAlign: "center" };

const GameSelect = () => {
  const router = useRouter();

  return (
    <>
      <div className='selectPage' style={{ display: "flex", gap: "24px" }}>

        {/* AIとチャット */}
        <div className='select-chat'>
          <Card sx={cardStyle}>
            <CardContent>

              {/* タイトル */}
              <div style={{ height: 96, textAlign: "center" }}>
                <Typography sx={{ color: 'text.secondary', fontSize: 48 }}>
                  AIとチャット
                </Typography>
              </div>

              {/* サブタイトル */}
              <div style={{ height: 48, textAlign: "center" }}>
                <Typography sx={{ color: 'text.secondary', fontSize: 24 }}>
                  ーサブタイトルー
                </Typography>
              </div>

              {/* 説明文 */}
              <div style={{ height: 288, overflow: "hidden", textAlign: "center" }}>
                <Typography sx={{ color: 'text.secondary', fontSize: 18, lineHeight: 1.4 }}>
                  ー説明ー<br />
                  ああああああああああああ<br />
                  ああああああああああああ<br />
                  ああああああああああああ<br />
                  ああああああああああああ<br />
                  ああああああああああああ<br />
                  ああああああああああああ<br />
                </Typography>
              </div>

            </CardContent>

            {/* ボタン */}
            <CardActions sx={{ justifyContent: "center", height: 48 }}>
              <Button onClick={() => router.push('/select/chat')}>
                Go ≫
              </Button>
            </CardActions>

          </Card>
        </div>

        {/* ゲームを検索 */}
        <div className='select-choose'>
          <Card sx={cardStyle}>
            <CardContent>

              <div style={{ height: 96, textAlign: "center" }}>
                <Typography sx={{ color: 'text.secondary', fontSize: 48 }}>
                  ゲームを検索
                </Typography>
              </div>

              <div style={{ height: 48, textAlign: "center" }}>
                <Typography sx={{ color: 'text.secondary', fontSize: 24 }}>
                  ーサブタイトルー
                </Typography>
              </div>

              <div style={{ height: 288, overflow: "hidden", textAlign: "center" }}>
                <Typography sx={{ color: 'text.secondary', fontSize: 18, lineHeight: 1.4 }}>
                  ー説明ー<br />
                  ああああああああああああ<br />
                  ああああああああああああ<br />
                  ああああああああああああ<br />
                  ああああああああああああ<br />
                  ああああああああああああ<br />
                  ああああああああああああ<br />
                </Typography>
              </div>

            </CardContent>

            <CardActions sx={{ justifyContent: "center", height: 48 }}>
              <Button onClick={() => router.push('/select/choose')}>
                Go ≫
              </Button>
            </CardActions>
          </Card>
        </div>

      </div>
    </>
  );
};

export default GameSelect;

