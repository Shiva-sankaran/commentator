import React, { useState } from 'react';

// Libs
import styled from 'styled-components';

// Styles
import {
    StyledBox,
    StyledTextField,
    StyledButton,
} from '../utils/styles';

const Login = props => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    return (
        <StyledBox
        component="form"
        sx={{
            '& > :not(style)': { m: 1 },
        }}
        noValidate
        autoComplete="off"
        >
            <StyledHeader>Login</StyledHeader>
            <StyledTextField id="login_username" label="username" variant="outlined" onChange={e => setUsername(e.target.value)}/>
            <StyledTextField id="login_password" label="password" variant="outlined" onChange={e => setPassword(e.target.value)} type='password'/>
            <StyledButton variant="contained">Submit</StyledButton>
        </StyledBox>
    );
};

export default Login;

const StyledHeader = styled.p`
    font-size: 40px;
    text-align: center;
    margin: auto;
    width: 100%;
    color: #333;
`;