import React from 'react';

interface ResponseViewerProps {
  response: unknown;
}

const ResponseViewer: React.FC<ResponseViewerProps> = ({ response }) => (
  <div className="mt-6 p-4 border rounded bg-gray-50 text-left max-w-xl mx-auto">
    <h3 className="text-xl font-bold mb-2">Analysis Result:</h3>
    <pre className="whitespace-pre-wrap text-sm">{JSON.stringify(response, null, 2)}</pre>
  </div>
);

export default ResponseViewer;