import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import CaptionFlowWrapper from './integrations/CaptionFlowWrapper';

// Import integrated apps
import SocialMediaClientApp from './integrations/SocialMediaClient/App';
import BrandProfileApp from './integrations/BrandProfile/App';

import React from 'react';

// Auth Guard Component
const RequireAuth = ({ children }: { children: React.ReactElement }) => {
  const location = useLocation();
  const isAuthenticated = localStorage.getItem('bloom_user') !== null;

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />

        {/* Hub Dashboard */}
        <Route path="/" element={
          <RequireAuth>
            <Dashboard />
          </RequireAuth>
        } />

        {/* Integrated Apps */}
        <Route path="/caption-flow" element={
          <RequireAuth>
            <CaptionFlowWrapper />
          </RequireAuth>
        } />

        <Route path="/social-media/*" element={
          <RequireAuth>
            <SocialMediaClientApp />
          </RequireAuth>
        } />

        <Route path="/brand-profile/*" element={
          <RequireAuth>
            <BrandProfileApp />
          </RequireAuth>
        } />

        {/* Catch all redirect to dashboard */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
