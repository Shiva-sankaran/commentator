import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { Route, Routes } from 'react-router';
import { createBrowserHistory } from 'history';

// PAGES
import Login from './Auth/Login';
import Signup from './Auth/Signup';
import Home from './Home/Home';

const Router = () => {
    const history = createBrowserHistory();

    return (
        <BrowserRouter history={history}>
            <Routes>
                <Route path="/login" exact element={<Login />} />
                <Route path="/signup" exact element={<Signup />} />
                <Route path="/" exact element={<Home />} />
            </Routes>
        </BrowserRouter>
    );
};

export default Router;