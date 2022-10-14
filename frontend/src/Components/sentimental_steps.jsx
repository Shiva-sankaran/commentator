import React from 'react';
import styled from 'styled-components';

const Sentimental_steps = () => {
    return (
        <StyledContainer>
            <StyledHeader>Steps to Follow!</StyledHeader>
            <StyledSteps>1. Select the emotion for the sentence.</StyledSteps>
            <StyledSteps>2. The selected emotion turns purple.</StyledSteps>
            <StyledSteps>3. Individual word depicting emotions get a default color.</StyledSteps>
            <StyledSteps>4. 'Positive' - green, 'Negative' - Red, 'Neutral' - Blue .</StyledSteps>
            <StyledSteps>5. Update individual word tags.</StyledSteps>
        </StyledContainer>
    );
};

export default Sentimental_steps;

const StyledContainer = styled.div`
    width: 100%;
    margin: 20px;
`;

const StyledHeader = styled.div`
    font-size: 28px;
`;

const StyledSteps = styled.div`
    font-size: 18px;
    margin: 8px auto;
`;