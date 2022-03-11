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
        { field: 'date', headerName: "Date", width: 100 },
        { field: 'sentence', headerName: "Sentence", flex: 1 },
        // { field: 'grammar', headerName: "Grammar", width: 100 },
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

        const dateFormtatter = d => {
            return (
                d.split('T')[0]
            );
        };

        result.map((elem) => {
            let sentence = "";
            console.log(elem[2]);
            elem[2].map(word => {sentence = sentence + word['key'] + " "})
            console.log(sentence);

            const row = {
                id: sid,
                date: dateFormtatter(elem[1]),
                sentence: sentence,
                // grammar: elem[0]
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
                    pageSize={15}
                    rowsPerPageOptions={[5]}
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
    cursor: pointer;
`;