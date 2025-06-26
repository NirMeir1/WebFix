import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import CtaTestDashboard from './pages/dashboard/CtaTestDashboard';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/dashboard/cta_test" element={<CtaTestDashboard />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);