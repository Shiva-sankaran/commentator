const detectURLs = (message) => {
  var urlRegex = /(((https?:\/\/)|(www\.))[^\s]+)/g;
  return message.match(urlRegex);
}

const EnglishSplitter = (sentence) => {
    // const sent = sentence.match(/\b(\w+)\b/g);
    const links = detectURLs(sentence) ? detectURLs(sentence) : [];
    console.log(links);
    let sent = sentence;

    links.map(link => {
        sent = sent.replace(link, "");
    });
    console.log(sent)
    sent = sent.match(/\b([\w+^']+)\b/g)
    console.log(sent);
    return {sent, links};
};

export default EnglishSplitter;