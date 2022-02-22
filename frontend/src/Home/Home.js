import React, { useState, useEffect } from 'react';

// Libs
import styled from 'styled-components';

// Components
import Navbar from '../Components/Navbar';
import LanguageBtn from '../Components/LanguageBtn';

// Utils
import LanguageDetect from '../utils/LanguageDetect';
import EnglishSplitter from '../utils/EnglishSplitter';
import HindiSplitter from '../utils/HindiSplitter';

const Home = props => {
    const [ selected, setSelected ] = useState('e');

    // const [words, setWords] = useState(wordArr);

    // const sentence = "Hi, this is Shubh. This is an Annotation tool.";
    const sentence = "नमस्ते, यह शुभ है। यह एक एनोटेशन टूल है।";

    // const words = EnglishSplitter(sentence);
    const {en, hi} = LanguageDetect(sentence);
    console.log('en: ', en, 'hi: ', hi);
    const wordArr = (sent) => {
        if(en > hi){
            return (EnglishSplitter(sent));
        } else {
            return (HindiSplitter(sent));
        }
    };
    const [words, setWords] = useState(wordArr(sentence));
    useEffect(() => {
        console.log(wordArr(sentence));
        setWords(wordArr(sentence));
    }, [sentence]);

    // console.log(HindiSplitter());
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
    }, [selected, words]);

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
            <StyledSentenceContainer>
                <StyledDisplaySentenceContainer>
                    {/* <StyledSentence>नमस्ते, यह शुभ है। यह एक एनोटेशन टूल है।</StyledSentence> */}
                    <StyledSentence>{sentence}</StyledSentence>
                </StyledDisplaySentenceContainer>
                <div>
                    <LanguageBtn selected={selected} setSelected={setSelected}/>
                </div>
            </StyledSentenceContainer>
            
            <div>
                <StyledWordBreakup>
                    Individual Word Tags
                </StyledWordBreakup>
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
            </div>
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
    font-size: 32px;
    margin: 12px;
    text-align: left;
    background-color: #efefef;
    padding: 18px;
    border-radius: 12px;
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

const StyledWordBreakup = styled.div`
    font-size: 20px;
    text-align: center;
    margin: 28px auto 12px auto;
`;

const StyledSentenceContainer = styled.div`
    border: 2px solid #efefef;
    padding: 24px;
    border-radius: 12px;
    width: max-content;
    text-align: center;
    margin: 24px auto;
`;