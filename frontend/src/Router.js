import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { Route, Routes } from 'react-router';
import { createBrowserHistory } from 'history';

// PAGES
import Login from './Auth/Login';
import Signup from './Auth/Signup';
import Home from './Home/Home';
import Admin from './Admin/Admin';

// COMPONENTS
import ProtectedRoute from './utils/ProtectedRoute';
import AdminRoute from './utils/AdminRoute';
import Intermediate from './Home/Intermediate';
import Profile from './User/Profile';
import Edit from './Edit/Edit';

const Router = () => {
    const history = createBrowserHistory();

    return (
        <BrowserRouter history={history}>
            <Routes>
                <Route path="/login" exact element={<Login />} />
                <Route path="/signup" exact element={<Signup />} />
                {/* <Route path="/" exact element={<ProtectedRoute />}>
                    <Route exact path='/intermediate' element={<Intermediate/>}/>
                </Route> */}
                <Route path="/admin" exact element={<AdminRoute />}>
                    <Route exact path='/admin' element={<Admin/>}/>
                </Route>
                <Route path="/" exact element={<ProtectedRoute />}>
                    <Route exact path='/profile' element={<Profile/>}/>
                    <Route exact path='/edit/:sid' element={<Edit/>}/>
                    <Route exact path='/intermediate' element={<Intermediate/>}/>
                    <Route exact path='/' element={<Home/>}/>
                </Route>
            </Routes>
        </BrowserRouter>
    );
};

export default Router;