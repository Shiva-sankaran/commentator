import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';

// Components
import Navbar from '../Components/Navbar';

const Admin = () => {
    const history = useNavigate();
    const [file, setFile] = useState();

    useEffect(() => {
        console.log(file);
    }, [file]);

    const [ userList, setUserList ] = useState([]);

    useEffect(() => {
        const fetchUsernames = async () => {
            const res = await axios.post('/fetch-users-list', {
                method: "POST",
                headers: {
                    'Content-type': 'application-json',
                    'Access-Control-Allow-Origin': '*',
                },
            });
            console.log(res.data.result);
            setUserList(res.data.result);
        };

        fetchUsernames();
    }, []);

    
    return (
        <div>
            <Navbar />
            <StyledFlexContainer>
                <form style={styledForm} method="POST" action="/admin-file-upload" enctype="multipart/form-data" >
                    <input type='file' name="file" onChange={e => setFile(e.target.files[0])}/>
                    <StyledButton style={styledButton} type="submit">Submit</StyledButton>
                </form>

                <StyledForm method="POST" action="/sentence-schema-creation" enctype="multipart/form-data" >
                    <StyledButton style={styledButton} type="submit">Create Schemas</StyledButton>
                </StyledForm>

                <StyledForm method="POST" action="/csv-download" enctype="multipart/form-data" >
                    <StyledTextInput type="text" name="username" placeholder='Enter username'>
                        {/* <option>opt</option> */}
                        {userList.map(elem => {
                            return (
                                <option value={elem} name="option_tag">
                                    {elem}
                                </option>
                            )
                        })}
                    </StyledTextInput>
                    <StyledButton style={styledButton} type="submit">Download csv</StyledButton>
                </StyledForm>
            </StyledFlexContainer>

            <StyledCompareForm method="POST" action="/compare-annotators" enctype="multipart/form-data" >
                <StyledFlexRow>
                    <StyledTextInput type="text" name="username1" placeholder='Enter username'>
                        {/* <option>opt</option> */}
                        {userList.map(elem => {
                            return (
                                <option value={elem} name="option_tag">
                                    {elem}
                                </option>
                            )
                        })}
                    </StyledTextInput>

                    <StyledTextInput type="text" name="username2" placeholder='Enter username'>
                        {/* <option>opt</option> */}
                        {userList.map(elem => {
                            return (
                                <option value={elem} name="option_tag">
                                    {elem}
                                </option>
                            )
                        })}
                    </StyledTextInput>
                </StyledFlexRow>
                <StyledButton style={styledButton} type="submit">Download Comparison csv</StyledButton>
            </StyledCompareForm>
        </div>
    );
};

export default Admin;

const styledButton = {
    color: '#fff',
};

const styledForm = {
    border: '2px solid #efefef',
    padding: '20px',
    borderRadius: '12px'
};

const StyledForm = styled.form`
    border: 2px solid #efefef;
    padding: 20px;
    border-radius: 12px;
`;

const StyledFlexContainer = styled.div`
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 20px;
`;

const StyledTextInput = styled.select`
    padding: 10px 8px;
    color: black;
    border: 2px solid #efefef;
    border-radius: 4px;
    width: 200px;
`;

const StyledButton = styled.button`
    background-color: #502380;
    color: white;
    border-radius: 8px;
    padding: 6px 16px;
    /* width: 65px; */
    height: 40px;
    text-transform: uppercase;
    border: none;
    min-width: 120px;

`;

const StyledFlexRow = styled.div`
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 12px;
    margin: 20px;
`;

const StyledCompareForm = styled.form`
    border: 2px solid #efefef;
    padding: 20px;
    border-radius: 12px;
    width: min-content;
    text-align: center;
    margin: 40px auto;
`;