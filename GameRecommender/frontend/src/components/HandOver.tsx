import axios from 'axios'
import React, { useState, useEffect } from 'react'


interface MessageResponse {
    message: string;
}

const Hand_over = () => {
    const [inputText, setInputElement] = useState("")//useState(初期値)
    const [text, setText] = useState("ここに表示されます")
    const [message, setMessage] = useState<string>("")
    useEffect(() => {
        axios.get<MessageResponse>('http://localhost:8000/')
            .then(response => {
                setMessage(response.data.message);
            })
            .catch(error => {
                console.error("Error fetching data:", error);
            });
    }, []);
    
    const printText = () => {
        if (inputText !== "") {
            setText(inputText + "/////" + message)//fastapiとreactのメッセージを結合
            setInputElement("")
        } else {
            setText("文字を入力してください")
        }
    }


    return (
        <div className="App">
            <header className="App-header">
                <h1>入力した文章を表示するアプリ</h1>
                <div className="print">
                    <p>{text}</p>
                </div>
                <div className="ctr">
                    <input value={inputText} onChange={(e) => setInputElement(e.target.value)} type="text" placeholder="入力してボタンを押してください。" />
                    <button onClick={printText}>表示する</button>
                </div>
            </header>
        </div>
    )
}

export default Hand_over