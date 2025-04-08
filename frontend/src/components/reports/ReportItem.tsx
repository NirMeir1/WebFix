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
    <div className="mb-4 rounded-lg overflow-hidden shadow-md w-full max-w-[1500px]">
      <div
        onClick={() => setExpanded(!expanded)}
        className="flex items-center justify-between cursor-pointer py-3 px-4 bg-blue-50 hover:bg-blue-100 transition-colors border-b w-full"
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
        <div className="p-6 bg-white text-gray-900 text-[17px] sm:text-[18px] font-normal sm:font-medium leading-[1.8] tracking-normal font-serif space-y-2">
          {content
            .split('\n')
            .map((line, i) => {
              // Replace starting dash(es) with bullet point and trim
              const cleanedLine = line.replace(/^\s*-{1,2}\s*/, '• ');

              // Split the line into parts to find bold segments
              const parts = cleanedLine.split(/(\*\*.*?\*\*)/g);

              return (
                <div key={i}>
                  {parts.map((part, index) =>
                    part.startsWith('**') && part.endsWith('**') ? (
                      <strong key={index}>{part.slice(2, -2)}</strong>
                    ) : (
                      <span key={index}>{part}</span>
                    )
                  )}
                </div>
              );
            })}
        </div>
      )}
    </div>
  );
};

export default ReportItem;