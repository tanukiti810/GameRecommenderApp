'use client';

import React, { useState } from 'react'
import '../../../app/globals.css'
import Title from '../Title'
import Slider from '@mui/material/Slider';
import Box from '@mui/material/Box';
import { Typography } from '@mui/material';

const priceMarks = [
    0, 500, 1000, 2000, 5000, 10000, 20000, 50000
];

const HeaderSelect = () => {
    const [rangeIndex, setRangeIndex] = useState<number[]>([0, 5]); // インデックスで管理

    const handleSliderChange = (event: Event, newValue: number | number[]) => {
        setRangeIndex(newValue as number[]);
    };

    return (
        <div className='liquid-glass-card-header'>
            <div className='header-outline flex' style={{ display: "flex", alignItems: "center", gap: "16px" }}>
                <Title />
                <div style={{
                    flex: 0.4,
                    color: 'white',
                    paddingRight: "10px"
                }}>
                    <Box>
                        <Typography variant="body1" sx={{ color: 'white', display: 'inline', ml: 1 }}>
                            ¥{priceMarks[rangeIndex[0]].toLocaleString()} 〜 ¥{priceMarks[rangeIndex[1]].toLocaleString()}
                        </Typography>

                        <Slider
                            value={rangeIndex}
                            onChange={handleSliderChange}
                            valueLabelDisplay="auto"
                            valueLabelFormat={(i) => `¥${priceMarks[i].toLocaleString()}`}
                            min={0}
                            max={priceMarks.length - 1}
                            marks={priceMarks.map((v, i) => ({ value: i, label: `¥${v.toLocaleString()}` }))}
                            step={1}
                        />
                    </Box>
                </div>

            </div>
        </div>
    );
}

export default HeaderSelect;
