"use client";

import { useEffect, useState } from "react";
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import CardActionArea from '@mui/material/CardActionArea';
import CardActions from '@mui/material/CardActions';
import '../../../app/globals.css';
import NumberWithComma from "@/components/common/NumberWithComma";

interface Game {
    id: number;
    title: string;
    description: string;
    image: string;
    price: number;
}

const SelectedGames = () => {
    const [games, setGames] = useState<Game[]>([]);

    useEffect(() => {
        const fetchGames = async () => {
            const res = await fetch("http://localhost:8000/api/games");
            const data = await res.json();

            // data は [{id, title, description, image}, ...] を想定
            setGames(data);
        };

        fetchGames();
    }, []);

    return (
        <div className='ChooseBox'>
            件数：{games.length}

            <div className="grid-container">
                {games.map((game) => (
                    <Card key={game.id} sx={{ maxWidth: 250 }}>
                        <CardActionArea component="a" target="blank" href={`https://store.steampowered.com/app/${game.id}`}>
                            <CardMedia
                                component="img"
                                height="140"
                                image={game.image}
                                alt={game.title}
                            />
                            <CardContent>
                                <Typography
                                    gutterBottom
                                    component="div"
                                    className="clamp-2 card-title"
                                >
                                    {game.title}
                                </Typography>
                                <Typography
                                    variant="body2"
                                    sx={{ color: "text.secondary" }}
                                    className="clamp-2 card-description"
                                >
                                    {game.description}
                                </Typography>
                            </CardContent>
                        </CardActionArea>
                        <CardActions className="card-bottom">
                            <Typography>
                                ￥
                                <NumberWithComma value={game.price} />
                            </Typography>
                            <Button size="small" color="primary" href={`https://store.steampowered.com/app/${game.id}`} target="_blank">
                                link ≫
                            </Button>
                        </CardActions>
                    </Card>
                ))}
            </div>
        </div>
    );
};

export default SelectedGames;
