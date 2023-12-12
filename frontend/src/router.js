import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useKeycloak } from '@react-keycloak/web';
import Login from './pages/Login'
import Upload from './pages/Upload'

const RequireAuth = ({ children, redirectTo }) => {
    const { keycloak } = useKeycloak();
    return keycloak.authenticated ? children : <Navigate to={redirectTo} />;
  };

const AppRouter = () => {
    return (
        <BrowserRouter>
            <Routes>
            <Route path="/" element={<Login />} />
            <Route
                path="/upload"
                element={
                    <RequireAuth redirectTo="/">
                        <Upload />
                    </RequireAuth>
                }
      />
            </Routes>
        </BrowserRouter>
    )
  }

export default AppRouter;