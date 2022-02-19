import React, { useState } from "react";

// Libs
import styled from 'styled-components';
import Alert from '@mui/material/Alert';

// Styles
import {
    StyledBox,
    StyledTextField,
    StyledButton,
} from '../utils/styles';


const Signup = props => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [showErr, setShowErr] = useState(false);



    const passwordMatcher = () => {
        console.log(password === confirmPassword);
        if(password === confirmPassword){
            setShowErr(false);
        } else {
            setShowErr(true);
        }
    };

    const onSubmitHandler = () => {
        passwordMatcher();
    };

    return (
        <StyledBox
        component="form"
        sx={{
            '& > :not(style)': { m: 1 },
        }}
        noValidate
        autoComplete="off"
        >
            <StyledHeader>Sign Up</StyledHeader>
            <StyledTextField id="login_username" label="username" variant="outlined" onChange={e => setUsername(e.target.value)}/>
            <StyledTextField id="login_password" label="password" variant="outlined" onChange={e => setPassword(e.target.value)} type='password'/>
            <StyledTextField id="login_confirm_password" label="confirm password" variant="outlined" onChange={e => setConfirmPassword(e.target.value)} type='password'/>
            {showErr && (<Alert severity="error">Password did not match, kindly re-enter.</Alert>)}
            <StyledButton variant="contained" onClick={onSubmitHandler}>Submit</StyledButton>
        </StyledBox>
    );
};

export default Signup;

const StyledHeader = styled.p`
    font-size: 40px;
    text-align: center;
    margin: auto;
    width: 100%;
    color: #333;
`;