import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import App from './App';
import './index.css';
import CtaTestDashboard from './pages/dashboard/CtaTestDashboard';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/dashboard/cta_test" element={<CtaTestDashboard />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
);
