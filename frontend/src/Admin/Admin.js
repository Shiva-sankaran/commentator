import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';

// Components
import Navbar from '../Components/Navbar';

import { TextField } from '@mui/material';

const Admin = () => {
    const history = useNavigate();
    const [file, setFile] = useState();

    useEffect(() => {
        console.log(file);
    }, [file]);

    const [ userList, setUserList ] = useState([]);
    const [kappa, setKappa] = useState(0);
    const [cmi, setCmi] = useState(0);

    useEffect(() => {
        const fetchUsernames = async () => {
            const res = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/fetch-users-list`, {
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

    const adminFileUpload = process.env.REACT_APP_BACKEND_URL + '/admin-file-upload'
    const csvDownload = process.env.REACT_APP_BACKEND_URL + '/csv-download'
    const compareAnnotators = process.env.REACT_APP_BACKEND_URL + '/compare-annotators'
    
    return (
        <div>
            <Navbar />
            <StyledFlexContainer>
                <form style={styledForm} method="POST" action={adminFileUpload} enctype="multipart/form-data" >
                    <input type='file' name="file" onChange={e => setFile(e.target.files[0])}/>
                    <StyledButton style={styledButton} type="submit">Submit</StyledButton>
                </form>

                {/* <StyledForm method="POST" action="/sentence-schema-creation" enctype="multipart/form-data" >
                    <StyledButton style={styledButton} type="submit">Create Schemas</StyledButton>
                </StyledForm> */}

                <StyledForm method="POST" action={csvDownload} enctype="multipart/form-data" >
                    <StyledTextInput type="text" name="username" placeholder='Enter username'>
                        {/* <option>opt</option> */}
                        <option value="ALL" name="option_tag" selected>
                                    ALL
                        </option>
                        {userList.map(elem => {
                            return (
                                <option value={elem} name="option_tag">
                                    {elem}
                                </option>
                            )
                        })}
                    </StyledTextInput>
                    <StyledKappa
                        name="cmi"
                        type='text'
                        placeholder='Enter CMI Threshold'
                        onChange={(e) => setCmi(e.target.value)}
                        required={true}
                        style={{ marginLeft: 12, marginRight: 12 }}
                    />
                    <StyledButton style={styledButton} type="submit">Download csv</StyledButton>
                </StyledForm>
            </StyledFlexContainer>

            <StyledCompareForm method="POST" action={compareAnnotators} enctype="multipart/form-data" >
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

                    <StyledKappa
                        name="kappa"
                        type='text'
                        placeholder='Enter Kappa Threshold'
                        onChange={(e) => setKappa(e.target.value)}
                        required={true}
                    />
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
    padding: 12px 8px;
    color: black;
    border: 2px solid #efefef;
    border-radius: 4px;
    width: 200px;
`;

const StyledKappa = styled.input`
    padding: 0px 8px !important;
    color: black !important;
    border: 2px solid #efefef !important;
    border-radius: 4px !important;
    width: 200px !important;
    height: 40.8px !important;
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