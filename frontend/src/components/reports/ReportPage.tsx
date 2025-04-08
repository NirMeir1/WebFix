import React from 'react';
import ReportDetails from './ReportDetails';
import PageLayout from '../layout/PageLayout';

interface ReportPageProps {
  url: string;
  response: string;
}

const ReportPage: React.FC<ReportPageProps> = ({ url, response }) => (
  <PageLayout>
    {/* Heading moved to left */}
    <div className="w-full px-8 pt-8">
      <h2 className="text-xl sm:text-2xl font-bold mb-4">
        CRO report for <a href={url} className="text-blue-500 underline break-words">{url}</a>
      </h2>
    </div>

    {/* Centered buttons */}
    <div className="flex justify-center gap-4 mb-6">
      <button className="bg-green-600 text-white font-semibold px-4 py-2 rounded shadow hover:bg-green-700 transition">Desktop</button>
      <button className="bg-green-600 text-white font-semibold px-4 py-2 rounded shadow hover:bg-green-700 transition">Mobile</button>
    </div>

    {/* Left-aligned report content */}
    <div className="px-8 pb-12">
      <ReportDetails reportText={response} />
    </div>
  </PageLayout>
);

export default ReportPage;