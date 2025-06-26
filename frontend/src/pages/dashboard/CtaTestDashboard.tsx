import React, { useEffect, useState } from 'react';

type Row = {variant:string, views:number, conversions:number, rate:number};

const CtaTestDashboard: React.FC = () => {
  const [rows, setRows] = useState<Row[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch('http://localhost:8000/results/cta_test');
        const data = await res.json();
        const arr = Object.keys(data).map(k => ({variant:k, ...data[k]}));
        setRows(arr);
      } catch(err){
        console.error(err);
      }
    };
    fetchData();
    const id = setInterval(fetchData, 10000);
    return () => clearInterval(id);
  }, []);

  const applyWinner = async () => {
    if(!rows.length) return;
    const winner = rows.reduce((a,b) => a.rate > b.rate ? a : b).variant;
    await fetch('http://localhost:8000/results/cta_test/publish', {
      method:'PUT',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({variant:winner})
    });
    alert(`Applied variant ${winner}`);
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">CTA Test Results</h1>
      <table className="min-w-full text-left">
        <thead>
          <tr>
            <th>Variant</th><th>Views</th><th>Conversions</th><th>Rate</th>
          </tr>
        </thead>
        <tbody>
          {rows.map(r => (
            <tr key={r.variant}>
              <td>{r.variant}</td>
              <td>{r.views}</td>
              <td>{r.conversions}</td>
              <td>{r.rate.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <button className="mt-4 p-2 bg-blue-500 text-white" onClick={applyWinner}>Apply Winning Variant</button>
    </div>
  );
};
export default CtaTestDashboard;
