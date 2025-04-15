import React from 'react';
import Loader from "./Loader";


interface UrlFormProps {
  url: string;
  industry: string;
  email: string;
  loading: boolean;
  reportType: 'basic' | 'deep';
  industries: string[];
  setUrl: React.Dispatch<React.SetStateAction<string>>;
  setIndustry: React.Dispatch<React.SetStateAction<string>>;
  setEmail: React.Dispatch<React.SetStateAction<string>>;
  setReportType: React.Dispatch<React.SetStateAction<'basic' | 'deep'>>;
  onSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
}

const UrlForm: React.FC<UrlFormProps> = ({
  url, industry, email, loading, reportType,
  industries, setUrl, setIndustry, setEmail, setReportType, onSubmit
}) => (
  <form onSubmit={onSubmit} className="max-w-xl mx-auto space-y-4 py-8">
    <input
      type="text"
      value={url}
      onChange={e => setUrl(e.target.value)}
      placeholder="Which URL would you like to analyze?"
      className="w-full p-3 border rounded shadow-md"
    />

    <select
      value={industry}
      onChange={e => setIndustry(e.target.value)}
      className="hidden" // Hidden if industry select is not visible in your design
    >
      {industries.map(opt => <option key={opt}>{opt}</option>)}
    </select>

    <input
      type="email"
      value={email}
      onChange={e => setEmail(e.target.value)}
      placeholder="Your Email"
      className="hidden" // Hidden if email field is only shown conditionally
    />

    <div className="flex flex-col gap-4 items-center">
      <div className="relative inline-block">
        <button
          type="submit"
          onClick={() => setReportType('basic')}
          disabled={loading}
          className={`relative w-64 py-3 px-4 rounded-full text-white font-bold text-lg shadow-lg text-center
            ${loading ? (reportType === 'basic' ? 'bg-gray-400' : 'bg-gray-200 cursor-not-allowed')
                      : 'bg-gradient-to-r from-green-400 to-green-600 hover:opacity-90'}`}
        >
          {loading && reportType === 'basic' ? 'Just A Sec...' : 'Basic Report'}

          {/* Tooltip trigger (question mark) */}
          <div className="absolute right-3 top-1/2 -translate-y-1/2 group">
            <span className="w-5 h-5 flex items-center justify-center rounded-full bg-white text-gray-800 text-xs font-bold cursor-default hover:bg-gray-100">
              ?
            </span>
            <div className="absolute bottom-full right-0 mb-2 hidden group-hover:flex w-72 bg-white text-gray-800 text-sm p-3 rounded-lg shadow-xl border z-10">
              <span>
                View a basic CRO report for your website -
                This report highlights 10 key issues to fix today or suggests improvements for an excellent score.
              </span>
            </div>
          </div>
        </button>
      </div>


      <div className="relative inline-block">
        <button
          type="submit"
          onClick={() => setReportType('deep')}
          disabled={loading}
          className={`relative w-64 py-3 px-4 rounded-full text-white font-bold text-lg shadow-lg text-center
            ${loading ? (reportType === 'deep' ? 'bg-gray-400' : 'bg-gray-200 cursor-not-allowed') 
                      : 'bg-gradient-to-r from-green-500 to-green-700 hover:opacity-90'}`}
        >
          {loading && reportType === 'deep' ? 'Just A Sec...' : 'Deep Report'}

          {/* Tooltip trigger (question mark) */}
          <div className="absolute right-3 top-1/2 -translate-y-1/2 group">
            <span className="w-5 h-5 flex items-center justify-center rounded-full bg-white text-gray-800 text-xs font-bold cursor-default hover:bg-gray-100">
              ?
            </span>
            <div className="absolute bottom-full right-0 mb-2 hidden group-hover:flex w-72 bg-white text-gray-800 text-sm p-3 rounded-lg shadow-xl border z-10">
              <span>
                The deep CRO report includes tailored insights, examples, and actionable recommendations to improve your site’s performance. Email verification required.
              </span>
            </div>
          </div>
        </button>
      </div>

      {loading && <Loader />}

      {!loading && (
        <span className="text-sm italic">
          For deep report we will need your email
        </span>
      )}

    </div>

    <div className="border-t pt-4 text-sm">
      The service is provided in two stages, <strong>both free</strong>. The first stage is a basic report, points.
      The extended report includes examples and recommendations, but to prevent malicious use of the website,
      we will ask you to confirm your identity by email.
    </div>

    <div className="border-t pt-4 text-sm">
      <strong>Our Story:</strong><br />
      We are a team of CRO and technology experts who believe that every website can improve.
      We founded Bottom Line to help website owners or those on their behalf understand the potential of their website
      and gain practical insights to improve conversion rates. Increasing your advertising budget is easy,
      but before that... what's going on at home?
    </div>
  </form>
);

export default UrlForm;