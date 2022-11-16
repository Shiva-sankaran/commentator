import React, { Component }  from 'react';
import '../css/POS.css';
import Navbar from '../Components/POS_navbar';
import Leftbox from '../Components/POS_Leftbox';


import { useState, useEffect } from 'react';



function POS() {

  const [text, textSet] = useState("");
  const [show, setShow] = useState(false);
  
  
  const [showedText, setShowedText] = useState("");
  const [data, setData] = useState([]);
  // let inputText = "";
  const writeText = (event)=>{
    textSet(event.target.value);
  }
  
 
  
 
  
  const generateTag = async ()=>{
    
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json','Authorization': 'Bearer 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' },
      body:JSON.stringify({'inputs': text})
      // body: JSON.stringify({ : 'React POST Request Example' })
    };
    fetch('https://api-inference.huggingface.co/models/sagorsarker/codeswitch-hineng-pos-lince',requestOptions)
    .then((response) => response.json())
      .then((data) => {
        setData(data);
      })
    // const res = await fetch('https://api-inference.huggingface.co/models/sagorsarker/codeswitch-hineng-pos-lince',requestOptions);
    // tags = await  res.json(); 
    console.log(data); 
   

}


const listItems = data.map(
    (element,index) => {
        return (
          <ul key={index} type="disc" style={{maxHeight: '100%', overflow: 'auto'}}>
              {element.word}
              <div style={{ 
                  fontWeight: 'bold', 
                  color: 'red' }}>
                    ({element.entity_group})
              </div>
              
          </ul>
        ) 
    }
  )


  return (
    <div className="App">
      <Navbar></Navbar>
      <Leftbox></Leftbox>
      {/* Take input from the user */}
      <div className='textAreaBox'>
      <textarea className='textArea' name="from-control" id="inputFromUsers" placeholder='Enter your text' cols="30" rows="14" value={text} onChange={writeText}></textarea>
      <button id='GenerateBtn' className='btn' onClick={generateTag}> Generate </button>
      </div>

      {/* Generate sentence */}
      <div className='generatedBox'>
        <h3>Individual POS Tag</h3> 
        {listItems}
        
      </div>
      

    </div>
  );
}

export default POS;