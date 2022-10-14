import axios from 'axios';

const FetchSentence = async () => {
    const id = JSON.parse(sessionStorage.getItem('annote_sentId')) + 1;
    const data = {
        id,
    };
    console.log("requesting backend for sentence")
    const res = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/get-sentence`, {
        method: "POST",
        headers: {
            'Content-type': 'application-json',
            'Access-Control-Allow-Origin': '*',
        },
        body: JSON.stringify(data)
    });
    console.log("WHOLE RESULT")
    console.log(res)
    console.log("!!!")
    console.log(res.data.result);
    return res.data.result;
};

export default FetchSentence;