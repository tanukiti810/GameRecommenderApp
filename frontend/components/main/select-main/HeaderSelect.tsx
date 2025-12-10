import React from 'react'
import '../../../app/globals.css'
import Title from '../Title'
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';

const HeaderSelect = () => {
    const [headData, setHeadData] = React.useState('');

    const handleChange = (event: SelectChangeEvent) => {
        setHeadData(event.target.value);
    };
    return (
        <div className='liquid-glass-card-header'>
            <div className='header-outline  flex'>
                <Title />
                <div>
                    {/* <FormControl sx={{ m: 1, minWidth: 120 }} size="small">
                        <InputLabel id="demo-select-small-label">Age</InputLabel>
                        <Select
                            labelId="demo-select-small-label"
                            id="demo-select-small"
                            value={headData}
                            label="type"
                            onChange={handleChange}
                        >
                            <MenuItem value="">
                                <em>None</em>
                            </MenuItem>
                            <MenuItem value={""}>マルチプレイヤー</MenuItem>
                            <MenuItem value={20}>Twenty</MenuItem>
                            <MenuItem value={30}>Thirty</MenuItem>
                        </Select>
                    </FormControl> */}
                </div>
            </div>
        </div>
    )
}

export default HeaderSelect