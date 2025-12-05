import React from 'react'
import SendIcon from '@mui/icons-material/Send';
const LiquidGlass = () => {
    return (
        <div className="background">
            <div className="liquid-glass-container">
                <div className="liquid-glass-card">
                    <input type="text" placeholder="Type your message..." className='liquid-glass-button' />
                    <button className="liquid-glass-button"><SendIcon /></button>
                </div>
            </div>
        </div>
    )

}

export default LiquidGlass