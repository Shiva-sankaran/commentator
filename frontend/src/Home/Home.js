import React, { useState, useEffect } from 'react';

// Libs
import styled from 'styled-components';

// Components
import Navbar from '../Components/Navbar';
import LanguageBtn from '../Components/LanguageBtn';

const Home = props => {
    const [ selected, setSelected ] = useState('e');

    const words = "Hi, this is Shubh. This is an Annotation tool.".match(/\b(\w+)\b/g);
    const [tag, setTag] = useState([]);

    useEffect(() => {
        const lst = [];
        let counter = 0;
        words.map(elem => lst.push({
            key: elem,
            value: selected,
            index: counter++,
        }));
        setTag(lst);
    }, [selected]);

    useEffect(() => {
        console.log(selected);
    }, [selected]);

    const toggle = letter => {
        if(letter === 'h'){
            return 'e';
        }
        else if (letter === 'e'){
            return 'h';
        }
    };

    useEffect(() => {
        console.log('TAG ARRAY: ', tag);
    }, [tag]);

    const updateTagForWord = word  => {
        // setTag([
        //     ...tag,
        //     tag[index] = {
        //         key: word.key,
        //         value: toggle(word.value)
        //     }
        // ]);
        let lst = [...tag];
        lst[word.index] = {
            key: word.key,
            value: toggle(word.value),
            index: word.index,
        }
        // console.log(lst);
        console.log('Selected', selected, 'Word_Value: ', toggle(word.value));
        setTag(lst);
        setSelected(selected);
    };

    return (
        <StyledContainer>
            <Navbar />
            <StyledDisplaySentenceContainer>
                {/* <StyledSentence>नमस्ते, यह शुभ है। यह एक एनोटेशन टूल है।</StyledSentence> */}
                <StyledSentence>Hi, this is Shubh. This is an Annotation tool.</StyledSentence>
            </StyledDisplaySentenceContainer>
            <div>
                <LanguageBtn selected={selected} setSelected={setSelected}/>
            </div>
            <StyledFlex>
                {tag.map(elem => {
                    console.log(selected, elem.value, selected === (elem.value));
                    return (
                        <StyledWord 
                        // style={{ backgroundColor: selected === elem.value ? 'green' : 'red' }}
                        lang={selected} individualTag={elem.value} key={elem.key} onClick={() => updateTagForWord(elem)}>{elem.key}</StyledWord>
                    );
                })}
            </StyledFlex>
        </StyledContainer>
    );
};

export default Home;

const StyledContainer = styled.div`
    height: 100%;
`;

const StyledDisplaySentenceContainer = styled.div`
    margin: 20px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
`;

const StyledSentence = styled.p`
    font-size: 26px;
    margin: 12px;
    text-align: left;
`;

const StyledFlex = styled.div`
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 6px;
    width: 75%;
    margin: 24px auto;
`;

const StyledWord = styled.div`
    border-radius: 8px;
    padding: 8px 8px;
    text-align: center;

    background-color: ${props => ((props.lang) === (props.individualTag)) ? '#71BC68' : '#B22B27'};
    cursor: pointer;
    display:flex;
    flex: 1;
    justify-content: center;
`;