import React, { useState, useEffect, useCallback } from 'react';
import axios, { AxiosError } from 'axios';
import UrlForm from './components/UrlForm';
import ReportPage from './components/reports/ReportPage';
import PageLayout from './components/layout/PageLayout';
import { ReportSchema } from './components/reports/ReportDetails';

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
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [report, setReport] = useState<ReportSchema | null>(null)
  const [reportType, setReportType] = useState<'basic' | 'deep'>('basic');
  const [message, setMessage] = useState('');
  const [showReport, setShowReport] = useState(false);
  const [screenshot, setScreenshot] = useState('');
  const [loadingMessage, setLoadingMessage] = useState('');
  const [isCached, setIsCached] = useState(false)


  useEffect(() => {
    axios.get('https://ghxfymbv44.execute-api.eu-north-1.amazonaws.com')
      .then(res => {
        if (res.data?.message) {
          setMessage(res.data.message);
        }
      })
      .catch(err => console.error(err));
  }, []);
  
  const handleSubmit = useCallback(async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError('');
    setReport(null);

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
      const res = await axios.post('https://ghxfymbv44.execute-api.eu-north-1.amazonaws.com/analyze-url', {
        url,
        ...(email && { email }),
        report_type: reportType,
      });

      const { output, screenshot_base64, is_cached } = res.data

      if (res.data.token) {
        localStorage.setItem('jwt', res.data.token);
      }
      
      const parsed: ReportSchema =
        typeof output === 'string' ? JSON.parse(output) : output;
      setReport(parsed);
      setScreenshot(`data:image/png;base64,${screenshot_base64}`) 
      setIsCached(is_cached)                                     // store the cache‐flag
      setShowReport(true)
      
    } catch (err) {
      const axiosError = err as AxiosError;
      setError('An error occurred while fetching data.');
      console.error(axiosError);
    } finally {
      setLoading(false);
    }
  }, [url, email, reportType]); 

  return (
    <>
      {!showReport ? (
        <PageLayout>
          <main className="flex-1 container mx-auto px-4 py-8 text-center">
            {message && <div className="mb-4 text-green-700 font-semibold text-lg">{message}</div>}
        
            <UrlForm
              url={url}
              email={email}
              loading={loading}
              loadingMessage={loadingMessage}
              reportType={reportType}
              setUrl={setUrl}
              setEmail={setEmail}
              setReportType={setReportType}
              onSubmit={handleSubmit}
            />
        
            {error && <p className="text-red-500 mt-4 font-semibold">{error}</p>}
          </main>
      </PageLayout>
      
      ) : (
        <ReportPage url={url} report={report!} screenshot={screenshot} isCached={isCached} reportType={reportType}/>
      )}
    </>
  );
};

export default App;