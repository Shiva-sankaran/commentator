import React from 'react'
import Navbar from '../Components/Navbar';
import styled from 'styled-components';


export const QnaPage = () => {
  return (
    <div>
        <Navbar />
        <div className="content" style={{marginTop:100, display:"flex", flexDirection:"row", justifyContent:"space-evenly"}}>
          <div style={{flex:2,borderRight:"1.5px solid grey", paddingLeft:20}}>

            <p style={{margin:0}}>
              <p style={{margin:0, fontSize:26}}>Steps to Follow</p>
              <p style={{margin:0, fontSize:21}}><br></br>1) Enter the context</p>
              <p style={{margin:0, fontSize:21}}>2) Enter the question</p>
              <p style={{margin:0, fontSize:21}}>3) Get the answer to the question</p>
              <p style={{margin:0, fontSize:21}}>4) Get answer!</p>
              <p style={{margin:0, fontSize:21}}>5) Switch between languages</p>
              <p style={{margin:0, fontSize:21}}>6) Save the annotations</p>
              <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
            </p>

          </div>
          <div style={{flex:5,marginLeft:20,paddingRight:50 }}>
          
              <p style={{margin:0, fontSize:35}}>Code Mixed Question Answering</p>

              <div>
              <p style={{margin:0, fontSize:25,marginTop:10}}>1) Enter the context:</p>
              <form style={{display:"flex",flexDirection:"column"}}>
                <label>
                  <input type="text" name="context" style = {{backgroundColor: "#D3D3D3", borderRadius: 7, width:"100%",height:60, marginTop:10,}}/><br/>
                </label>
                {/* <input type="submit" value="Submit" style={{marginTop:10, backgroundColor:"rgba(80, 35, 128, 0.9)", color:"White", height:30,borderRadius:10,width:100,fontSize:17,alignSelf:"center"}}/> */}
              </form>
              </div>

              <div>
              <p style={{margin:0, fontSize:25,marginTop:10}}>2) Enter the question:</p>
              <form style={{display:"flex",flexDirection:"column"}}>
                <label>
                  <input type="text" name="context" style = {{backgroundColor: "#D3D3D3", borderRadius: 7, width:"100%",height:60, marginTop:10,}}/><br/>
                </label>
                <input type="submit" value="SUBMIT" style={{marginTop:10, backgroundColor:"rgba(80, 35, 128, 0.9)", color:"White", height:40,borderRadius:10,width:100,fontSize:17,alignSelf:"center"}}/>
              </form>
              </div>

              <div>
              <p style={{margin:0, fontSize:25,marginTop:10}}>3) The answer:</p>
              <form style={{display:"flex",flexDirection:"column"}}>
                <label>
                  <input type="text" name="context" style = {{backgroundColor: "#D3D3D3", borderRadius: 7, width:"100%",height:60, marginTop:10,}}/><br/>
                </label>
                <input type="submit" value="ANNOTATE" style={{marginTop:10, backgroundColor:"rgba(80, 35, 128, 0.9)", color:"White", height:40,borderRadius:10,width:150,fontSize:17,alignSelf:"center"}}/>
                <input type="submit" value="SAVE ANNOTATIONS" style={{marginTop:20, backgroundColor:"rgba(80, 35, 128, 0.9)", color:"White", height:40,borderRadius:10,width:250,fontSize:17,alignSelf:"center"}}/>
              </form>
              </div>


          </div>
        </div>
    </div>
  )
}


export default QnaPage;

