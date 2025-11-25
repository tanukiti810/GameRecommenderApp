'use client'
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import './globals.css'

const page = () => {
  return (
    <div className='Main'>
      <div className='main-left text'>
        <h1 id='text'>FOR<br></br>ALL GAMERS</h1>
      </div>
      <div className='main-right'>
        <Card sx={{
          maxWidth: 350,
          width: '90%',
          padding: 2,
          bgcolor: '#fbfcfffa'
        }}>
          <CardContent>
            <Typography gutterBottom sx={{ color: '#2B262E', fontSize: '2rem' }}>
              説明<br />
              aaaaaaaaaaaaaa<br></br>
              aaaaaaaaaaaaaa<br></br>
              aaaaaaaaaaaaaa<br></br>
              aaaaaaaaaaaaaa<br></br>
              aaaaaaaaaaaaaa<br></br>
            </Typography>
          </CardContent>
          <CardActions>
            <a href='/select'>好きなゲームを探しに　≫</a>
          </CardActions>
        </Card>
      </div>
    </div>
  )
}

export default page

