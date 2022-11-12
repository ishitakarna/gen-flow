import React, {useState} from 'react';
import PropTypes from 'prop-types';
import './Login.scss';
import Api from "../../api";
import {Button, Form} from "react-bootstrap";

export default function Login({setToken}) {
    const [username, setUserName] = useState();
    const [password, setPassword] = useState();

    const handleSubmit = async e => {
        e.preventDefault();
        const api = new Api();
        let token = null
        api.loginUser(username, password).then( res => {
            let resp = res.data
            if(resp.status === false){
                alert("Incorrect Email or Password")
            } else {
                setToken(token)
                sessionStorage.setItem("token", JSON.stringify(resp))
            }
        })
    }
    return (
        <div className="login-wrapper">
            <h1>Log In</h1>
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3" controlId="formBasicEmail">
                    <Form.Label>Email</Form.Label>
                    <Form.Control type="email" placeholder="Enter Email" onChange={e => setUserName(e.target.value)}/>
                </Form.Group>

                <Form.Group className="mb-3" controlId="formBasicPassword">
                    <Form.Label>Password</Form.Label>
                    <Form.Control type="password" placeholder="Password" onChange={e => setPassword(e.target.value)}/>
                </Form.Group>
                <Button variant="primary" type="submit">
                    Submit
                </Button>
            </Form>
        </div>
    )
}

Login.propTypes = {
    setToken: PropTypes.func.isRequired
}