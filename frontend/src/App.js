import './App.css';
import React, { useState } from 'react';
import Login from "./components/Login/Login";
import ProcessOwnerView from './components/ProcessOwnerView/ProcessOwnerView';
import BusinessOwnerView from './components/BusinessOwnerView/BusinessOwnerView';

function App() {
    const [token, setToken] = useState();

    if(!token && !sessionStorage.getItem("token")) {
        return <Login setToken={setToken} />
    }
    else {
        let savedToken = JSON.parse(sessionStorage.getItem("token"))
        let userType = savedToken.user.userType
        let businessName = savedToken.business.businessName
        let userId = savedToken.user.userId
        let userName = savedToken.user.fName + " " + savedToken.user.lName
        console.log(savedToken)
        if(userType === "business-owner"){
            return (
                <div className="App">
                    <BusinessOwnerView bName={businessName}/>
                </div>
            );
        } else {
            return (
                <div className="App">
                    <ProcessOwnerView 
                    businessName={businessName}
                    userId = {userId}
                    userName = {userName}/>
                </div>
            );
        }
    }
}

export default App;
