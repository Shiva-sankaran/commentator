import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';
import Navbar from '../Components/Navbar';

const Profile = () => {
    const history = useNavigate();
    const [rows, setRows] = useState([{
        id: 0, sentence: 'Dummy Sentence', grammar: 'e'
    }]);

    const columns = [
        { field: 'id', headerName: "Sentence ID", width: 100 },
        { field: 'date', headerName: "Date", width: 200 },
        { field: 'sentence', headerName: "Sentence", width: 800 },
        { field: 'grammar', headerName: "Grammar", width: 100 },
    ];

    const fetchAllSentences = async () => {
        const username = sessionStorage.getItem('annote_username');
        const data = {
            username
        };
        const res = axios.post('/all-sentences', {
            method: "POST",
            headers: {
              "Content-type": "application-json",
              "Access-Control-Allow-Origin": "*",
            },
            body: JSON.stringify(data),
        });

        console.log(await res);
        let result = await res;
        result = result.data.result;
        console.log(result);

        let rowArr = [];
        let sid = 1;
        result.map((elem) => {
            let sentence = "";
            console.log(elem[2]);
            elem[2].map(word => {sentence = sentence + word['key'] + " "})
            console.log(sentence);
            const row = {
                id: sid,
                date: elem[1],
                sentence: sentence,
                grammar: elem[0]
            };
            sid = sid + 1;
            console.log(row);
            rowArr.push(row);
        });
        setRows(rowArr);
    };

    useEffect(() => {
        fetchAllSentences();
    }, []);

    useEffect(() => {
        console.log(rows);
    }, [rows]);

    return (
        <div>
            <Navbar />
            <StyledDataGridContainer>
                {rows.length > 0 && (<DataGrid
                    rows={rows}
                    columns={columns}
                    pageSize={5}
                    rowsPerPageOptions={[5]}
                    checkboxSelection
                    onRowClick={(param) => history(`/edit/${param.row.id}`)}
                />)}      
            </StyledDataGridContainer>
        </div>
    );
};

export default Profile;

const StyledDataGridContainer = styled.div`
    height: 80vh;
    width: 90%;
    /* padding: 24px; */
    margin: 32px auto;
    overflow-x: hidden;
`;