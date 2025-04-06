import React, { useState } from 'react';

interface ReportItemProps {
  title: string;
  rating: 'green' | 'orange' | 'yellow' | 'red';
  content: string;
}

const ratingColors = {
  green: 'bg-green-400',
  orange: 'bg-orange-400',
  yellow: 'bg-yellow-400',
  red: 'bg-red-500',
};

const ReportItem: React.FC<ReportItemProps> = ({ title, rating, content }) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <div>
      <div
        onClick={() => setExpanded(!expanded)}
        className="flex items-center justify-between cursor-pointer py-3 border-b"
      >
        <div className="flex items-center">
          <span className="text-lg font-semibold mr-2">+</span>
          <span>{title}</span>
        </div>
        <div className={`w-8 h-8 rounded-full ${ratingColors[rating]}`}></div>
      </div>

      {expanded && (
        <div className="p-4 text-gray-600 text-sm bg-gray-100">
          {content} {/* Display dynamic content here */}
        </div>
      )}
    </div>
  );
};

export default ReportItem;