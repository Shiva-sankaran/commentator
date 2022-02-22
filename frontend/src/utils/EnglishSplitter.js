const EnglishSplitter = (sentence) => {
    return sentence.match(/\b(\w+)\b/g);
};

export default EnglishSplitter;