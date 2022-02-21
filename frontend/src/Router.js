import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { Route, Routes } from 'react-router';
import { createBrowserHistory } from 'history';

// PAGES
import Login from './Auth/Login';
import Signup from './Auth/Signup';
import Home from './Home/Home';

// COMPONENTS
import ProtectedRoute from './utils/ProtectedRoute';

const Router = () => {
    const history = createBrowserHistory();

    return (
        <BrowserRouter history={history}>
            <Routes>
                <Route path="/login" exact element={<Login />} />
                <Route path="/signup" exact element={<Signup />} />
                <Route path="/" exact element={<ProtectedRoute />}>
                    <Route exact path='/' element={<Home/>}/>
                </Route>
            </Routes>
        </BrowserRouter>
    );
};

export default Router;