import React, { useState } from 'react';
import PageLayout from '../layout/PageLayout';
import { ArrowLeft } from 'lucide-react';
import ReportDetails, { ReportSchema } from './ReportDetails';

interface ReportPageProps {
  url: string;
  report: ReportSchema;
  screenshot: string;
  isCached: boolean;
  reportType: 'basic' | 'deep';
}

const ReportPage: React.FC<ReportPageProps> = ({ url, report, screenshot, isCached, reportType }) => {
  const [view, setView] = useState<'desktop' | 'mobile'>('desktop');
  const topActions = React.useMemo(() => {
    const seen = new Set<string>();
    const actions: string[] = [];
    Object.values(report.pages).forEach(page => {
      ['desktop', 'mobile'].forEach(dev => {
        page[dev].recommendations.forEach(rec => {
          if (!seen.has(rec)) {
            seen.add(rec);
            actions.push(rec);
          }
        });
      });
    });
    return actions.slice(0, 5);
  }, [report]);

  return (
    <PageLayout>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 px-8 pt-8 pb-12">
        {/* Left Column (Report Content) */}
        <div className="lg:col-span-2 space-y-6">
          {/* Back Button */}
          <button
            onClick={() => window.location.reload()}
            className="flex items-center text-blue-600 hover:text-blue-800 font-medium mb-4"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Take me back
          </button>

          {/* URL Heading */}
          <h2 className="text-xl sm:text-2xl font-bold">
            CRO report for{' '}
            <a href={url} className="text-blue-500 underline break-words">
              {url}
            </a>
          </h2>
          <p className="mt-2 font-medium">Overall CRO Score: {report.overall_score}</p>
          <p className="mb-4 text-gray-700 text-base sm:text-lg">{report.overall_observations}</p>

          {topActions.length > 0 && (
            <div className="bg-blue-50 p-4 rounded-md mb-4">
              <h3 className="font-semibold mb-2">What to fix first</h3>
              <ul className="list-disc pl-5 space-y-1 text-gray-800">
                {topActions.map((a, i) => (
                  <li key={i}>{a}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Device Toggle Buttons */}
          <div className="flex gap-4 mt-2">
            <button
              onClick={() => setView('desktop')}
              className={`px-4 py-2 rounded shadow font-semibold transition ${
                view === 'desktop' ? 'bg-green-600 text-white' : 'bg-gray-200 text-gray-800'
              }`}
            >
              Desktop
            </button>
            <button
              onClick={() => setView('mobile')}
              className={`px-4 py-2 rounded shadow font-semibold transition ${
                view === 'mobile' ? 'bg-green-600 text-white' : 'bg-gray-200 text-gray-800'
              }`}
            >
              Mobile
            </button>
          </div>

          {/* Report Sections */}
          <ReportDetails report={report as ReportSchema} view={view} isCached={isCached} reportType={reportType}/>

          <div className="mt-6 p-4 bg-green-50 rounded-md text-center">
            Need help implementing these fixes?{' '}
            <a href="#" className="text-green-700 underline">Contact us or upgrade for expert assistance.</a>
          </div>
        </div>

        {/* Right Column (Screenshot Placeholder) */}
        <div className="hidden lg:block">
          <div className="border rounded-2xl shadow-lg overflow-hidden">
            <div className="bg-gray-100 text-center py-2 font-medium text-gray-600">
              Mobile Screenshot
            </div>
            <div className="aspect-[9/16] bg-gray-200 flex items-center justify-center text-gray-500 rounded-xl overflow-hidden shadow">
              {!screenshot ? (
                'Loading...'
              ) : (
                <img src={screenshot} alt="Screenshot" className="object-cover w-full h-full" />
              )}
            </div>
          </div>
        </div>
      </div>
    </PageLayout>
  );
};

export default ReportPage;
