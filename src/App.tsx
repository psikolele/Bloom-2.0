import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import CaptionFlowWrapper from './integrations/CaptionFlowWrapper';

// Import integrated apps
// Note: These need to be exported as default components from their respective files
import SocialMediaClientApp from './integrations/SocialMediaClient/App';
import BrandProfileApp from './integrations/BrandProfile/App';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Hub Dashboard */}
        <Route path="/" element={<Dashboard />} />

        {/* Integrated Apps */}
        {/* Caption Flow - Iframe Wrapper */}
        <Route path="/caption-flow" element={<CaptionFlowWrapper />} />

        {/* Social Media Client - Full App Route */}
        {/* using /* to allow sub-routes if defined in the child app, though usually single page */}
        <Route path="/social-media/*" element={<SocialMediaClientApp />} />

        {/* Brand Profile - Full App Route */}
        <Route path="/brand-profile/*" element={<BrandProfileApp />} />

        {/* Catch all redirect to dashboard */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
