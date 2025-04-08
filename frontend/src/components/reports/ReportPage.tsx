import React from 'react';
import ReportDetails from './ReportDetails';
import PageLayout from '../layout/PageLayout';

interface ReportPageProps {
  url: string;
  response: string;
}

const ReportPage: React.FC<ReportPageProps> = ({ url, response }) => (
  <PageLayout>
    <div className="flex flex-col items-center px-4 py-8">
      <div className="w-full max-w-4xl bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl sm:text-2xl font-bold text-center mb-6">
          CRO report for <a href={url} className="text-blue-500 underline break-words">{url}</a>
        </h2>

        <div className="flex justify-center gap-4 mb-6 flex-wrap">
          <button className="bg-green-600 text-white font-semibold px-4 py-2 rounded shadow hover:bg-green-700 transition">Desktop</button>
          <button className="bg-green-600 text-white font-semibold px-4 py-2 rounded shadow hover:bg-green-700 transition">Mobile</button>
        </div>

        <ReportDetails reportText={response} />
      </div>
    </div>
  </PageLayout>
);

export default ReportPage;