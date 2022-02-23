import axios from 'axios';

const FetchSentence = async () => {
    const id = 50
    const data = {
        id,
    };
    const res = await axios.post('/get-sentence', {
        method: "POST",
        headers: {
            'Content-type': 'application-json',
            'Access-Control-Allow-Origin': '*',
        },
        body: JSON.stringify(data)
    });
    console.log(res);
    return res;
};

export default FetchSentence;