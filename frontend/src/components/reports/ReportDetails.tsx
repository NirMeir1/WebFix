import React from 'react';
import ReportItem from './ReportItem';

const sections: { title: string; rating: 'green' | 'orange' | 'yellow' | 'red'; content: string }[] = [
    { title: 'HOME PAGE', rating: 'green', content: 'The home page is the most important page of your website. It should be designed to capture the attention of visitors and guide them to take action.' },
    { title: 'Category Page', rating: 'orange', content: 'The category page is where users can browse products by category. It should be designed to help users find what they are looking for quickly and easily.' },
    { title: 'Product Page', rating: 'yellow', content: 'The product page is where users can view detailed information about a product. It should be designed to provide all the information users need to make a purchase decision.' },
    { title: 'Checkout Page', rating: 'red', content: 'The checkout page is where users complete their purchase. It should be designed to minimize friction and make the process as smooth as possible.' },
    { title: 'Navigation', rating: 'orange', content: 'The navigation menu is the primary way users move around your site. It should be designed to be intuitive and easy to use.' },
    { title: 'Summary', rating: 'orange', content: 'The summary section provides a quick overview of the report. It should be designed to highlight the most important findings and recommendations.' },
  ];
  

const ReportDetails: React.FC = () => (
  <div className="border-t border-gray-200">
    {sections.map(section => (
      <ReportItem key={section.title} title={section.title} rating={section.rating} content={section.content} />
    ))}
  </div>
);

export default ReportDetails;