import React from 'react';
import Header from '../Header';
import Footer from '../Footer';
import ReportDetails from './ReportDetails';

interface ReportPageProps {
  url: string;
  response: string;
}

const ReportPage: React.FC<ReportPageProps> = ({ url, response }) => (
  <div className="flex flex-col min-h-screen">
    <Header />
    
    <main className="flex-1 container mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold text-left mb-4">
        CRO report for <a href={url} className="text-blue-500 underline">{url}</a>
      </h2>

      <ReportDetails reportText={response}/>
    </main>

    <Footer />
  </div>
);

export default ReportPage;