import React from 'react';
import Loader from "./Loader";
import TooltipButton from './TooltipButton';

interface UrlFormProps {
  url: string;
  email: string;
  loading: boolean;
  reportType: 'basic' | 'deep';
  loadingMessage: string;
  setUrl: React.Dispatch<React.SetStateAction<string>>;
  setEmail: React.Dispatch<React.SetStateAction<string>>;
  setReportType: React.Dispatch<React.SetStateAction<'basic' | 'deep'>>;
  onSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
}

const UrlForm: React.FC<UrlFormProps> = ({
  url, email, loading, reportType, 
  loadingMessage, setUrl, setEmail, setReportType, onSubmit
}) => (
  <form onSubmit={onSubmit} className="max-w-xl mx-auto space-y-4 py-8">
    <input
      type="text"
      value={url}
      onChange={e => setUrl(e.target.value)}
      placeholder="Which URL would you like to analyze?"
      className="w-full p-3 border rounded shadow-md"
    />

    <input
      type="email"
      value={email}
      onChange={e => setEmail(e.target.value)}
      placeholder="Your Email"
      className="hidden" // Hidden if email field is only shown conditionally
    />

    <div className="flex flex-col gap-4 items-center">
      <TooltipButton
        text="Basic Report"
        tooltip="View a basic CRO report for your website - This report highlights 10 key issues to fix today or suggests improvements for an excellent score."
        onClick={() => setReportType('basic')}
        disabled={loading}
        isLoading={loading}
        isActive={reportType === 'basic'}
        gradientClass="bg-gradient-to-r from-green-400 to-green-600 hover:opacity-90"
      />

      <TooltipButton
        text="Deep Report"
        tooltip="The deep CRO report includes tailored insights, examples, and actionable recommendations to improve your site’s performance. Email verification required."
        onClick={() => setReportType('deep')}
        disabled={loading}
        isLoading={loading}
        isActive={reportType === 'deep'}
        gradientClass="bg-gradient-to-r from-green-500 to-green-700 hover:opacity-90"
      />

      {loading && <Loader message={loadingMessage} />}

      {!loading && (
        <span className="text-lg font-bold italic">
          For the deep report, we will need your email.
        </span>
      )}

    </div>

    <div className="border-t pt-4 text-base">
      Our service is offered in two stages, <strong>both free.</strong> 
      The basic report gives an overview of your website's performance. 
      For a more comprehensive analysis, the deep report dives deeper, 
      offering valuable insights and actionable recommendations that can significantly enhance your website’s Conversion Rate Optimization (CRO) potential.
    </div>

    <div className="border-t pt-4 text-base">
      <strong>Our Story:</strong><br />
      We are a team of CRO and technology experts who believe that every website can improve. 
      We founded Bottom Line to help website owners—or those acting on their behalf—understand
      the potential of their website and gain practical insights to improve conversion rates. 
      Increasing your advertising budget is easy, but before that... what's going on at home?
    </div>
  </form>
);

export default UrlForm;