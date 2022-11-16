import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { Route, Routes } from 'react-router';
import { createBrowserHistory } from 'history';

// PAGES
import Login from './Auth/Login';
import Signup from './Auth/Signup';
import Home from './Home/Home';
import Sentiment from './Home/Sentiment'
import QnaPage from './Home/QNA'
import Admin from './Admin/Admin';
import POS from './Home/POS'  
import Sent_qual from './Home/Sent_qual'  
import Summ from './Home/Summarize'  
import ProtectedRoute from './utils/ProtectedRoute';
import AdminRoute from './utils/AdminRoute';
import Intermediate from './Home/Intermediate';
import Profile from './User/Profile';
import Edit from './Edit/Edit';
import NER from './NER/ner';

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
                    <Route exact path='/sentiment' element={<Sentiment/>}/>
                    <Route exact path='/QNA' element={<QnaPage/>}/>
                    <Route exact path='/SentQ' element={<Sent_qual/>}/>
                    <Route exact path='/POS' element={<POS/>}/>
                    <Route exact path='/NER' element={<NER/>}/>
                    <Route exact path='/Summ' element={<Summ/>}/>
                    <Route exact path='/' element={<Home/>}/>
                </Route>
            </Routes>
        </BrowserRouter>
    );
};

export default Router;