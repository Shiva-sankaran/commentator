import React from 'react';
import Steps from '../Components/Steps';
import styled from 'styled-components';
import { StyledButton } from '../utils/styles';
import { useNavigate } from 'react-router-dom';

const Intermediate = () => {
    const history = useNavigate();
    const onSubmitHandler = () => {
        history('/');
    };
    return (
        <StyledContainer>
            <Steps />
            <StyledButton style={{ margin: 'auto 20px' }} variant="contained" onClick={onSubmitHandler}>Continue</StyledButton>
        </StyledContainer>
    );
};

export default Intermediate;

const StyledContainer = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    width: 50%;
    margin: auto;
`;