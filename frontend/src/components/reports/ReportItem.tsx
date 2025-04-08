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
    <div className="mb-4 rounded-lg overflow-hidden shadow-lg">
      <div
        onClick={() => setExpanded(!expanded)}
        className="flex items-center justify-between cursor-pointer py-3 px-4 bg-blue-50 hover:bg-blue-100 transition-colors border-b"
      >
        <div className="flex items-center">
          {/* Rotate the plus icon when expanded */}
          <span
            className={`text-base sm:text-lg font-semibold text-gray-800 ${
              expanded ? 'rotate-45' : ''
            }`}
          >
            +
          </span>
          <span className="text-xl font-medium">{title}</span>
        </div>
        <div className={`w-6 h-6 sm:w-7 sm:h-7 rounded-full ${ratingColors[rating]}`}></div>
      </div>

      {expanded && (
        <div className="p-4 bg-white text-gray-700 text-base font-sans leading-relaxed">
          {content} {/* Display the content when expanded */} 
        </div>
      )}
    </div>
  );
};

export default ReportItem;