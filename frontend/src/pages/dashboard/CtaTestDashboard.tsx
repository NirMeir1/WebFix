import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface ResultRow {
  views: number;
  conversions: number;
  rate: string;
}

const CtaTestDashboard: React.FC = () => {
  const [data, setData] = useState<Record<string, ResultRow>>({});

  useEffect(() => {
    const fetchData = () => {
      axios.get('http://localhost:8001/results/cta_test')
        .then(res => setData(res.data))
        .catch(console.error);
    };
    fetchData();
    const id = setInterval(fetchData, 10000);
    return () => clearInterval(id);
  }, []);

  const applyWinner = async () => {
    if (!data) return;
    const winner = Object.entries(data).sort((a,b)=>{
      const ar = parseFloat(a[1].rate); const br = parseFloat(b[1].rate); return br-ar;})[0][0];
    await axios.put('http://localhost:8001/results/cta_test/publish', null, { params: { winner } });
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">CTA Test Results</h1>
      <table className="min-w-full text-left">
        <thead>
          <tr><th>Variant</th><th>Views</th><th>Conversions</th><th>Rate</th></tr>
        </thead>
        <tbody>
          {Object.entries(data).map(([variant,row]) => (
            <tr key={variant} className="border-b"><td>{variant}</td><td>{row.views}</td><td>{row.conversions}</td><td>{row.rate}</td></tr>
          ))}
        </tbody>
      </table>
      <button className="mt-4 px-3 py-2 bg-blue-500 text-white" onClick={applyWinner}>Apply Winner</button>
    </div>
  );
};
export default CtaTestDashboard;
