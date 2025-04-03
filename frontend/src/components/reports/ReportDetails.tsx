import React from 'react';
import ReportItem from './ReportItem';

const sections: { title: string; rating: 'green' | 'orange' | 'yellow' | 'red' }[] = [
    { title: 'HOME PAGE', rating: 'green' },
    { title: 'Category Page', rating: 'orange' },
    { title: 'Product Page', rating: 'yellow' },
    { title: 'Checkout Page', rating: 'red' },
    { title: 'Navigation', rating: 'orange' },
    { title: 'Summary', rating: 'orange' },
  ];
  

const ReportDetails: React.FC = () => (
  <div className="border-t border-gray-200">
    {sections.map(section => (
      <ReportItem key={section.title} title={section.title} rating={section.rating} />
    ))}
  </div>
);

export default ReportDetails;