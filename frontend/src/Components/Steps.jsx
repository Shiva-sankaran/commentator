import React from 'react';
import styled from 'styled-components';

const Steps = () => {
    return (
        <StyledContainer>
            <StyledHeader>Steps to Follow!</StyledHeader>
            <StyledSteps>1. Select Matrix Language for the sentence.</StyledSteps>
            <StyledSteps>2. The selected grammar turns purple.</StyledSteps>
            <StyledSteps>3. Individual word tags get a default color.</StyledSteps>
            <StyledSteps>4. 'English' - green, 'Hindi' - yellow, 'Unidentified' - blue .</StyledSteps>
            <StyledSteps>5. Update individual word tags.</StyledSteps>
        </StyledContainer>
    );
};

export default Steps;

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