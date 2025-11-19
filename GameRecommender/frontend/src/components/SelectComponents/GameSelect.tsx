import React from 'react'
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import '../../App.css'
import { useNavigate } from 'react-router-dom';

const GameSelect = () => {
    const navigate = useNavigate();
    
    return (
        <>
            <div>Select page</div>
            <Box sx={{
                '& button': {
                    m: 5,
                    borderWidth: 3,
                    fontSize: '0.9rem',
                    padding: '14px 36px',
                    width: '300px',
                    height: '100px'
                }
            }}>
                <div className='ButtonBox'>
                    <div className='BoxContainer'>
                        <Button variant="outlined" className='largeButton' onClick={() => navigate('/Chat')}>
                            Wanna Find Out??
                            <br></br>
                            Let's Chat!!
                        </Button>
                        <Button variant="outlined" className='largeButton' onClick={() => navigate('/Choose')}>
                            wanna choose questions
                            <br></br>
                            your like??
                        </Button>
                    </div>
                </div>
            </Box>
        </>
    )
}

export default GameSelect