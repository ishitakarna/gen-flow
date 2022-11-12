import './App.css';
import React, { useState } from 'react';
import Login from "./components/Login/Login";
import ProcessOwnerView from './components/ProcessOwnerView/ProcessOwnerView';
import BusinessOwnerView from './components/BusinessOwnerView/BusinessOwnerView';

function App() {
    const [token, setToken] = useState();

    // if(!token) {
    //     return <Login setToken={setToken} />
    // }
    return (
        <div className="App">
            <ProcessOwnerView/>
        </div>
    );
}

export default App;
