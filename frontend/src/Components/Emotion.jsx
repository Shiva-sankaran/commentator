import React, { useState } from 'react';

import styled from 'styled-components';

const LanguageBtn = ({ selected, setSelected }) => {
    return (
        <StyledFlexer>
            <StyledPosBtn lang={selected} onClick={() => setSelected('p')}>Positive</StyledPosBtn>
            <StyledNegBtn lang={selected} onClick={() => setSelected('n')}>Negative</StyledNegBtn>
            <StyledNeuBtn lang={selected} onClick={() => setSelected('i')}>Neutral</StyledNeuBtn>

        </StyledFlexer>
    );
};

export default LanguageBtn;

const StyledFlexer = styled.div`
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 12px;
`;

const StyledPosBtn = styled.div`
    border-radius: 8px;
    padding: 8px 4px;
    width: 100px;
    text-align: center;

    background-color: ${props => props.lang === 'p' ? '#502380' : '#efefef'};
    color: ${props => props.lang === 'p' ? '#efefef' : '#333'};
    cursor: pointer;
`;

const StyledNegBtn = styled.div`
    border-radius: 8px;
    padding: 8px 4px;
    width: 100px;
    text-align: center;

    background-color: ${props => props.lang === 'n' ? '#502380' : '#efefef'};
    color: ${props => props.lang === 'n' ? '#efefef' : '#333'};
    cursor: pointer;
`;

const StyledNeuBtn = styled.div`
    border-radius: 8px;
    padding: 8px 4px;
    width: 100px;
    text-align: center;

    background-color: ${props => props.lang === 'i' ? '#502380' : '#efefef'};
    color: ${props => props.lang === 'i' ? '#efefef' : '#333'};
    cursor: pointer;
`;