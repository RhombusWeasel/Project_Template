import { BrowserRouter as Router, Route, Navigate, Routes } from "react-router-dom";
import LandingPage from './templates/pages/landing_page/LandingPage';
import PasswordResetForm from './templates/forms/PasswordResetForm';
import AdminPage from './templates/pages/admin_page/AdminPage';
import UserHome from './templates/pages/user_home/UserHome';
import RegisterForm from './templates/forms/RegisterForm';
import NavBar from './templates/reusable/navbar/NavBar';
import LoginForm from './templates/forms/LoginForm';
import React, { useState, useEffect } from 'react';
import Logout from "./templates/forms/Logout";
import AdminConsole from "./utils/admin";
import './App.css';

const App = () => {
  const [isLoggedIn, setLoggedIn] = useState(false);
  const [permissions, setPermissions] = useState({
    'admin': false,
    'trusted': false,
    'user': true
  });

  useEffect(() => {
    if (isLoggedIn && permissions.admin) {
      window.admin = new AdminConsole();
    }
  }, [isLoggedIn, permissions]);

  return (
    <Router>
      <div className='App'>
        <NavBar
          isLoggedIn={isLoggedIn}
          permissions={permissions}
        />
        <div className='App-body'>
          <Routes className='App-body'>
            <Route
              exact path="/"
              element={isLoggedIn
                ? <UserHome permissions={permissions} />
                : <LandingPage />}
            />
            <Route
              path="/login"
              element={isLoggedIn ? <Navigate to="/" /> : <LoginForm setLoggedIn={setLoggedIn} setPermissions={setPermissions} />}
            />
            <Route
              path="/register"
              element={<RegisterForm />}
            />
            <Route
              path="/reset-password"
              element={<PasswordResetForm />}
            />
            <Route
              path="/logout"
              element={<Logout setLoggedIn={setLoggedIn} setPermissions={setPermissions} />}
            />
            <Route
              path="/admin"
              element={permissions.admin ? <AdminPage /> : <Navigate to="/" />}
            />
            {/* Additional routes can be placed here, don't forget to add them to the NavBar if they need it. */}
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;