import axios from 'axios';

const FetchSentence = async () => {
    const id = JSON.parse(sessionStorage.getItem('annote_sentId')) + 1;
    const data = {
        id,
    };
    const res = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/get-sentence`, {
        method: "POST",
        headers: {
            'Content-type': 'application-json',
            'Access-Control-Allow-Origin': '*',
        },
        body: JSON.stringify(data)
    });
    console.log(res.data.result);
    return res.data.result;
};

export default FetchSentence;