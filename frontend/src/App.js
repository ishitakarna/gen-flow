import './App.css';
import React, { useState } from 'react';
import Login from "./components/Login/Login";

function App() {
    const [token, setToken] = useState();

    if(!token) {
        return <Login setToken={setToken} />
    }
    return (
        <div className="App">
            <header className="App-header">

            </header>
        </div>
    );
}

export default App;
