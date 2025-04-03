import React, { useState, useCallback, useEffect, useRef } from 'react';
import axios, { AxiosError } from 'axios';

// Define a type for the expected API response.
interface ApiResponse {
    type: 'Z' | 'A' | 'B';
    message: string;
    token?: string;
  // Extend with more fields as needed.
}

// List of industries.
const industries = [
  'Technology',
  'Finance',
  'Healthcare',
  'Education',
  'Fashion',
  'Other'
];

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
  const [response, setResponse] = useState<ApiResponse | null>(null);
  const [reportType, setReportType] = useState<'basic' | 'deep'>('basic');
  const [message, setMessage] = useState(''); // Add this line

  const formRef = useRef<HTMLFormElement>(null);

  useEffect(() => {
    // Update this URL to match your FastAPI backend URL
    axios.get('http://127.0.0.1:8000')
      .then(response => {
        setMessage(response.data.message);
      })
      .catch(error => {
        console.error("There was an error fetching the message!", error);
      });
  }, []);

  // Submit handler using a form submission event.
  const handleSubmit = useCallback(async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError('');
    setResponse(null);

    if (!reportType || (reportType !== 'basic' && reportType !== 'deep')) {
      setError('Invalid report type.');
      return;
    }

    if (reportType === 'deep' && !email) {
      setError('Email is required for a deep report.');
      return;
    }
    
    // Validate URL.
    if (!isValidUrl(url)) {
      setError('Please enter a valid URL.');
      return;
    }
    
    // Validate email for deep report.
    if (reportType === 'deep' && !email) {
      setError('Email is required for a deep report.');
      return;
    }
      
    const normalizedIndustry = (industry === 'Other' ? 'e-commerce' : industry.toLowerCase());

    // Set up headers. Include JWT in deep report requests if available.
    const headers: Record<string, string> = {};
    if (reportType === 'deep') {
        const token = localStorage.getItem('jwt');
        if (token) {
        headers.Authorization = `Bearer ${token}`;
        }
    }

    setLoading(true);
    try {
        console.log({
          url,
          industry: normalizedIndustry,
          email,
          reportType
        });
        const res = await axios.post('http://127.0.0.1:8000/analyze-url', {
            url,
            industry: normalizedIndustry,
            email,
            report_type: reportType
            });
        const data: ApiResponse = res.data;

        if (data.token) {
            localStorage.setItem('jwt', data.token);
          }
          
      setResponse(data);

    } catch (err) {
      const axiosError = err as AxiosError;

      setError('An error occurred while fetching the data.');
      console.error('Request failed:', axiosError);

      if (axiosError.response) {
        console.error('Status:', axiosError.response.status);
        console.error('Data:', axiosError.response.data);
      }
    } finally {
      setLoading(false);
    }
  }, [url, industry, email, reportType]);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl mb-4">URL Analysis</h1>

      {/* Render the message here */}
      <h1>{message}</h1>  {/* Display the message from the backend */}

      <form ref={formRef} onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="url" className="block text-lg">
            URL:
          </label>
          <input
            type="text"
            id="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="w-full p-2 border rounded"
            placeholder="https://example.com"
          />
        </div>
        <div>
          <label htmlFor="industry" className="block text-lg">
            Industry:
          </label>
          <select
            id="industry"
            value={industry}
            onChange={(e) => setIndustry(e.target.value)}
            className="w-full p-2 border rounded"
          >
            {industries.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="email" className="block text-lg">
            Email (required for deep report):
          </label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full p-2 border rounded"
            placeholder="your.email@example.com"
          />
        </div>
        <div className="flex space-x-4">
          <button
            type="button"
            disabled={loading}
            onClick={() => {
              setReportType('basic');
              setTimeout(() => formRef.current?.requestSubmit(), 0);
            }}
            className="bg-blue-500 text-white p-2 rounded"
          >
            {loading ? 'Just a sec...' : 'Basic Report'}
          </button>

          <button
            type="button"
            disabled={loading}
            onClick={() => {
              setReportType('deep');
              setTimeout(() => formRef.current?.requestSubmit(), 0);
            }}
            className="bg-green-500 text-white p-2 rounded"
          >
            {loading ? 'Just a sec...' : 'Deep Report'}
          </button>
        </div>

      </form>
      {error && <p className="text-red-500 mt-4">{error}</p>}
      {response && (
        <div className="mt-4 p-4 border rounded">
          <h2 className="text-xl">Response:</h2>
          <pre className="whitespace-pre-wrap">{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default App;