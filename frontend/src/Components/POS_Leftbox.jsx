import React from 'react'
import '../css/POS.css';
// import '../css/'
import Button from "./POS_Button"

function Leftbox() {
    const data = [{
        text: "NOUN (nouns) ",
        color: "#fad",
    },
    {
        text: "PROPN(proper noun)",
        color: "#3EE419",
    },
    {
        text: "VERB (verbs)",
        color: "green",
    },
    {
        text: "ADJ (adjectives)",
        color: "red",
    },
    {
        text: "ADV (adverbs)",
        color: "#ACE95B",
    },
    {
        text: "ADP (prepositions and postpositions)",
        color: "#D74222",
    },
    {
        text: "PRON (pronouns)",
        color: "#E256D5",
    },
    {
        text: "DET (determiners/articles)",
        color: "red",
    },
    {
        text: "CONJ (conjunctions)",
        color: "#92B050",
    },
    {
        text: " PART",
        color: "#19E4AE",
    },
    {
        text: "PRON_WH",
        color: "#8A12D3",
    },
    {
        text: "PART_NEG",
        color: "#2AA9BB",
    },
    {
        text: "NUM",
        color: "#C6DA2D",
    },
    {
        text: "X (a catch-all)",
        color: "#6A4BD3",
    }
];
  return (
    <>
        <div className='leftBox'>
            <div className='btnBox'>
                {data.map((val, ind) => {

                    return (
                        <Button key={ind} text={val.text} color={val.color}/ >
                    )
                })}

            </div>
            
           
        </div>
    </>
    
  )
}

export default Leftbox