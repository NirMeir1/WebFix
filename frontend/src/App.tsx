import React, { useState, useEffect, useCallback } from 'react';
import axios, { AxiosError } from 'axios';
import UrlForm from './components/UrlForm';
import ReportPage from './components/reports/ReportPage';
import PageLayout from './components/layout/PageLayout';

// Define your industries once and pass them as props
const industries = ['Technology', 'Finance', 'Healthcare', 'Education', 'Fashion', 'Other'];

// Simple URL validator using the URL constructor.
const isValidUrl = (url: string): boolean => {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
};

const App: React.FC = () => {
  const [url, setUrl] = useState('');
  const [industry, setIndustry] = useState(industries[0]);
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [response, setResponse] = useState<string | null>(null);
  const [reportType, setReportType] = useState<'basic' | 'deep'>('basic');
  const [message, setMessage] = useState('');
  const [showReport, setShowReport] = useState(false);
  const [screenshot, setScreenshot] = useState('');
  const [loadingMessage, setLoadingMessage] = useState('');


  // Fetch an initial backend message (optional)
  useEffect(() => {
    axios.get('http://127.0.0.1:8000')
      .then(res => setMessage(res.data.message))
      .catch(err => console.error(err));
  }, []);

  // Handle form submission logic
  const handleSubmit = useCallback(async (e: React.FormEvent<HTMLFormElement>) => {
    console.log('Submitting...');
    e.preventDefault();
    setError('');
    setResponse(null);

    // Validate URL.
    if (!isValidUrl(url)) {
      setError('Please enter a valid URL.');
      return;
    }

    // Uncomment the following lines if you want to enforce email for deep report

    // Basic validation for deep report type.
    // if (reportType === 'deep' && !email) {
    //   setError('Email is required for a deep report.');
    //   return;
    // }

    setLoadingMessage("Running CRO magic on your site, it may take a few seconds...");
    setLoading(true);
    setShowReport(false);  // Reset report display

    try {
      const res = await axios.post('http://127.0.0.1:8000/analyze-url', {
        url,
        industry: industry === 'Other' ? 'e-commerce' : industry.toLowerCase(),
        ...(email && { email }),
        report_type: reportType,
      });

      if (res.data.token) {
        localStorage.setItem('jwt', res.data.token);
      }

      setResponse(res.data);
      setScreenshot(`data:image/png;base64,${res.data.screenshot_base64}`);
      setShowReport(true);  // Show report after successful fetch
      
    } catch (err) {
      const axiosError = err as AxiosError;
      setError('An error occurred while fetching data.');
      console.error(axiosError);
    } finally {
      setLoading(false);
    }
  }, [url, industry, email, reportType]); 

  return (
    <>
      {!showReport ? (
        <PageLayout>
          <main className="flex-1 container mx-auto px-4 py-8 text-center">
            {message && <div className="mb-4 text-green-700 font-semibold text-lg">{message}</div>}
        
            <UrlForm
              url={url}
              industry={industry}
              email={email}
              loading={loading}
              loadingMessage={loadingMessage}
              reportType={reportType}
              industries={industries}
              setUrl={setUrl}
              setIndustry={setIndustry}
              setEmail={setEmail}
              setReportType={setReportType}
              onSubmit={handleSubmit}
            />
        
            {error && <p className="text-red-500 mt-4 font-semibold">{error}</p>}
          </main>
      </PageLayout>
      
      ) : (
        <ReportPage url={url} response={response || ''} screenshot={screenshot} />
      )}
    </>
  );
};

export default App;