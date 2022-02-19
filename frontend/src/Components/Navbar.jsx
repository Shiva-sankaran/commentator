import React from 'react';

// Libs
import styled from 'styled-components';
import { PowerSettingsNew } from '@mui/icons-material';

const Navbar = () => {
    return (
        <StyledNavbarContainer>
            <StyledName>Annotex</StyledName>
            <StyledPowerOff />
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
`;

const StyledName = styled.p`
    color: #fefefe;
    font-size: 26px;
    margin-left: 16px;
`;

const StyledPowerOff = styled(PowerSettingsNew)`
    margin-right: 16px;
    color: #fefefe;
`;