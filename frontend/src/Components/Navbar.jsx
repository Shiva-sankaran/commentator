import React from 'react';

// Libs
import styled from 'styled-components';
import { PowerSettingsNew } from '@mui/icons-material';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Navbar = () => {
    const history = useNavigate();
    const logged_in_user = JSON.parse(sessionStorage.getItem('annote_username'));
    const logoutHandler = async () => {

        const res = await axios.post('/logout', {
            method: "POST",
            headers: {
                'Content-type': 'application-json',
                'Access-Control-Allow-Origin': '*',
            },
        });
        // const resFinal = await res;
        console.log(res.data);
        sessionStorage.setItem('annote_user', false)
        sessionStorage.setItem('annote_username', "")
        sessionStorage.setItem('annote_sentId', 0)
        sessionStorage.setItem('annote_admin', false)
        history('/login');
        // fetch('/signup', {
        //     method: 'POST',
        //     headers: {
        //       'Content-type': 'application-json'
        //     },
        //     body: JSON.stringify(data)
        //   })
        //   .then(res => res.json())
        //   .then(res => console.log(res))
        //   .catch(err => console.log(err));
    };
    return (
        <StyledNavbarContainer>
            <StyledName onClick={() => history('/')}>Annotex</StyledName>
            <StyledFlex>
                <StyledUsername onClick={() => history('/profile')} style={{ cursor: 'pointer' }}>{logged_in_user}</StyledUsername>
                <StyledPowerOff onClick={logoutHandler}/>
            </StyledFlex>
        </StyledNavbarContainer>
    );
};

export default Navbar;

const StyledNavbarContainer = styled.div`
    position: fixed;
    top: 0;
    background-color: rgba(80, 35, 128, 0.9);
    width: 100%;
    height: 60px;

    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;

    z-index: 0;
`;

const StyledName = styled.p`
    color: #fefefe;
    font-size: 26px;
    margin-left: 16px;
    cursor: pointer;
`;

const StyledPowerOff = styled(PowerSettingsNew)`
    margin-right: 16px;
    color: #fefefe;
    cursor: pointer;
`;

const StyledFlex = styled.div`
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 24px;
`;

const StyledUsername = styled.div`
    color: #efefef;
    border-bottom: 1px solid #efefef;
    padding-bottom: 6px;
`;