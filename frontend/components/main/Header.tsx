'use client'

import { Button } from '@mui/material'
import { useRouter } from 'next/navigation'
import Title from './Title'

const Header = () => {
    const router = useRouter();
    return (    
        <div className='liquid-glass-card-header'>
            <div className='header-outline'>
                <Title />
                {/* <div>
                    <Button className='Filled-Button' variant="contained" onClick={() => router.push('/sign-in')}>Sign In/Up</Button>
                </div> */}
            </div>
        </div>
    )
}

export default Header