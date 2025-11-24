'use client'

import { Button } from '@mui/material'
import { useRouter } from 'next/navigation'
import React from 'react'
import '../../app/globals.css'
import Title from './Title'

const Header = () => {
    const router = useRouter();
    return (
        <div className='header'>
            <div className='header-outline  flex'>
                <Title />
                <div>
                    <Button className='Filled-Button' variant="contained" onClick={() => router.push('/sign-in')}>Sign In/Up</Button>
                </div>
            </div>
        </div>
    )
}

export default Header