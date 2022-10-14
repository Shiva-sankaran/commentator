import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

// Libs
import styled from 'styled-components';
import axios from 'axios';

// Components
import Navbar from '../Components/Navbar';
// import LanguageBtn from '../Components/LanguageBtn';
import Emotion from '../Components/Emotion'

// Utils
import LanguageDetect from '../utils/LanguageDetect';
import EnglishSplitter from '../utils/EnglishSplitter';
import HindiSplitter from '../utils/HindiSplitter';
import FetchSentence from '../utils/FetchSentence';

import { StyledButton } from '../utils/styles';
import Steps from '../Components/Steps';
import Sentimental_steps from '../Components/sentimental_steps';

const Sentimental = props => {
    const history = useNavigate();
    const [sentence, setSentence] = useState('Loading Sentence...');
    const [sentId, setSentId] = useState('');
    const [hypertext, setHypertext] = useState([]);
    const [hashtags, setHashtags] = useState([]);
    useEffect(() => {
        const x = async () => {
            const dict = await FetchSentence();
            console.log("FETCHING SENTENCE")
            console.log(dict['sentence'], dict['sentId'])
            setSentence(dict['sentence']);
            setSentId(dict['sentId'])
            console.log("SENTENCE ID SETTED")
            console.log(sentId)
            console.log(sentence)
        };
        x();
    }, []);

    const [ selected, setSelected ] = useState('');
    const startTime = new Date();

    // const sentence = "Hi, this is Shubh. This is an Annotation tool.";
    // const sentence = "नमस्ते, यह शुभ है। यह एक एनोटेशन टूल है।";

    const {en, hi} = LanguageDetect(sentence.length > 0 ? sentence : "");
    // console.log('en: ', en, 'hi: ', hi);
    const wordArr = (sent) => {
        if(en > hi){
            return (EnglishSplitter(sent));
        } else {
            return (HindiSplitter(sent));
        }
    };
    const [words, setWords] = useState(sentence.length > 0 ? wordArr(sentence) : wordArr(""));
    
    useEffect(() => {
        if(sentence.length > 0){
            let {sent, links, hashs} = wordArr(sentence);
            // console.log(sent);
            // console.log(links);
            // console.log(hashs);
            setWords(sent);
            setHypertext(links);
            setHashtags(hashs);
        }
    }, [sentence]);

    useEffect(() => {
        // console.log(hypertext);
    }, [hypertext]);

    const [tag, setTag] = useState([]);

    // useEffect(() => {
    //     // const lst = [];
    //     // let counter = 0;
    //     // words.map(elem => lst.push({
    //     //     key: elem,
    //     //     value: selected,
    //     //     index: counter++,
    //     // }));
    //     // setTag(lst);

    //     const fetchLidData = async () => {
    //         const data = {
    //             sentId
    //         };
    //         const res = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/get-lid-data`, {
    //             method: "POST",
    //             headers: {
    //                 'Content-type': 'application-json',
    //                 'Access-Control-Allow-Origin': '*',
    //             },
    //             body: JSON.stringify(data)
    //         });
    //         console.log(res.data.result);
    //         const resp = res.data.result;

    //         const lst = [];
    //         let counter = 0;
    //         resp.map(elem => lst.push({
    //             key: elem[0],
    //             value: 'p',
    //             index: counter++,
    //         }));
    //         console.log("LIDDDDDDDDDDDDDDD")
    //         console.log(resp)
    //         console.log(lst)
    //         setTag(lst);
    //     };
    //     fetchLidData();

    // }, [selected, words]);

    useEffect(() => {
        // const lst = [];
        // let counter = 0;
        // words.map(elem => lst.push({
        //     key: elem,
        //     value: selected,
        //     index: counter++,
        // }));
        // setTag(lst);
        const fetchSentimentData = async () => {
            const data = {
                sentId
            };
            
            const res = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/get-sentiment-data`, {
                method: "POST",
                headers: {
                    'Content-type': 'application-json',
                    'Access-Control-Allow-Origin': '*',
                },
                body: JSON.stringify(data)
            });
            console.log("SOMETHING SOMETHING")

            // const words_resp = res.data.words_tags
            console.log(res.data.result)
            const sent_resp = res.data.result[0];
            const words_resp = res.data.result[1]
            console.log("PREDICTED SENTIMENT")
            console.log(sent_resp)

            console.log("PREDICTED WORDS EMOT")
            console.log(words_resp)
            

            const lst = [];
            let counter = 0;
            words_resp.map(elem => lst.push({
                key: elem[0],
                value: elem[1],
                index: counter++,
            }));
            console.log("SEEEEEEEEEEEEEEEENN")
            console.log(lst)
            setTag(lst);
            setSelected(sent_resp)
            console.log("FETCHED SENTIMENTAL DATA")
            console.log(selected)
        };
        fetchSentimentData();

    }, [selected,words]);

    useEffect(() => {
        console.log(selected);
    }, [selected]);

    const toggle = letter => {
        if(letter === 'p'){
            return 'n';
        }
        else if (letter === 'n'){
            return 'i';
        } else if(letter === 'i'){
            return 'p';
        }
    };

    useEffect(() => {
        // console.log('TAG ARRAY: ', tag);
    }, [tag]);

    const updateTagForWord = word  => {
        let lst = [...tag];
        lst[word.index] = {
            key: word.key,
            value: toggle(word.value),
            index: word.index,
        }
        // console.log('Selected', selected, 'Word_Value: ', toggle(word.value));
        setTag(lst);
        setSelected(selected);
    };

    const onSubmitHandler = async () => {
        const username = JSON.parse(sessionStorage.getItem('annote_username'));
        const date = new Date();
        const endTime = new Date();

        const timeDifference = (endTime.getTime() - startTime.getTime()) / 1000;
        // console.log(timeDifference);

        const data = {
            selected,
            tag,
            sentId,
            username,
            date,
            hashtags,
            hypertext,
            timeDifference,
        };
        const res = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/submit-sentence`, {
            method: "POST",
            headers: {
                'Content-type': 'application-json',
                'Access-Control-Allow-Origin': '*',
            },
            body: JSON.stringify(data)
        });
        // console.log(res);
        sessionStorage.setItem('annote_sentId', sentId)
        window.location.reload()
    };

    return (
        <StyledContainer>
            <Navbar />
            <StyledGridder>
                <Sentimental_steps />
                <StyledRightContainer>
                    <StyledSentenceId>#{sentId}</StyledSentenceId>
                    <StyledSentenceContainer>
                        <StyledDisplaySentenceContainer>
                            {/* <StyledSentence>नमस्ते, यह शुभ है। यह एक एनोटेशन टूल है।</StyledSentence> */}
                            <StyledSentence>{sentence}</StyledSentence>
                        </StyledDisplaySentenceContainer>
                        <div>
                            <Emotion selected={selected} setSelected={setSelected}/>
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

                    <StyledSubmitContainer>
                        <StyledButton style={{ width: '100%' }} variant="contained" onClick={onSubmitHandler}>Submit</StyledButton>
                    </StyledSubmitContainer>
                </StyledRightContainer>
            </StyledGridder>
        </StyledContainer>
    );
};

export default Sentimental;

const StyledContainer = styled.div`
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
`;

const StyledGridder = styled.div`
    display: grid;
    grid-template-columns: 1fr 4fr;
    gap: 20px;
    overflow-y: auto;
    /* margin: */
`;

const StyledRightContainer = styled.div`
    border-left: 3px solid #efefef;
    margin-left: 12px;;
`;

const StyledDisplaySentenceContainer = styled.div`
    margin: 2px;
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
    flex-wrap: wrap;
`;

const StyledWord = styled.div`
    border-radius: 8px;
    padding: 8px 8px;
    text-align: center;

    background-color: ${props => ((props.individualTag) === 'p') ? '#00FF00 ' : '#D4DCE9'};
    background-color: ${props => ((props.individualTag) === 'n') && '#FF0000'};
    cursor: pointer;
    display:flex;
    flex: 0 1 10%;
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
    width: 90%;
`;

const StyledSubmitContainer = styled.div`
    width: 20%;
    text-align: center;
    margin: 40px auto;
`;

const StyledSentenceId = styled.div`
    background-color: #efefef;
    border-radius: 12px;
    padding: 12px;
    position: fixed;
    top: 75px;
    right: 20px;
`;