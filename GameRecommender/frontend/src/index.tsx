import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
// import './App.css'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import Nomatch from './components/Nomatch';
import SignIn from './components/SignIn';
import SignUp from './components/SignUp';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/Sign-In" element={<SignIn />} />
        <Route path="/Sign-Up" element={<SignUp />} />
        <Route path="/Nomatch" element={<Nomatch />} />
      </Routes>
    </Router>
  </React.StrictMode>
);
