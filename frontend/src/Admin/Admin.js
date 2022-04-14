import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

// Components
import Navbar from '../Components/Navbar';

const Admin = () => {
    const history = useNavigate();
    const [file, setFile] = useState();

    useEffect(() => {
        console.log(file);
    }, [file]);

    
    return (
        <div>
            <Navbar />
            <form method="POST" action="/admin-file-upload" enctype="multipart/form-data" >
                <input type='file' name="file" onChange={e => setFile(e.target.files[0])}/>
                <button type="submit">Submit</button>
            </form>

            <form method="POST" action="/sentence-schema-creation" enctype="multipart/form-data" >
                <button type="submit">Create Schemas</button>
            </form>
        </div>
    );
};

export default Admin;