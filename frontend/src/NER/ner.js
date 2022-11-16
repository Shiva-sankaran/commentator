import React, { useEffect } from "react";
import styled from 'styled-components';
// import { BrowserRouter } from "react-router-dom";
// import { Route, Routes } from "react-router";
// import { createBrowserHistory } from "history";

import Navbar from "../Components/Navbar";

const NER = () => {
  const createMarkup = () => {
    const frame = `<iframe style="width: 100%; height: 100%;" src="embed.html" title="NER"></iframe>`;
    return { __html: frame };
  };

  return (
    <>
      <Navbar />
      <StyledIframe dangerouslySetInnerHTML={createMarkup()}></StyledIframe>
    </>
  );
};

export default NER;

const StyledIframe = styled.div`
  width: 100%;
  height: 100vh;
`;