import React, { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';

interface ReportItemProps {
  title: string;
  content: string;
  score: number;
  colorClass: string;
}

const ReportItem: React.FC<ReportItemProps> = ({ title, content, score, colorClass }) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="mb-4 rounded-lg overflow-hidden shadow-md w-full max-w-[1500px]">
      <div
        onClick={() => setExpanded(!expanded)}
        className="flex items-center justify-between cursor-pointer py-3 px-4 bg-blue-50 hover:bg-blue-100 transition-colors border-b w-full"
      >
        <div className="text-xl font-medium text-gray-800">{title}</div>
        <div className="flex items-center gap-4">
          {expanded ? (
            <ChevronUp className="w-5 h-5 text-gray-700" />
          ) : (
            <ChevronDown className="w-5 h-5 text-gray-700" />
          )}
          <div className={`relative w-8 h-8 sm:w-9 sm:h-9 rounded-full ${colorClass} flex items-center justify-center text-white font-bold text-sm`}>
            {score}
          </div>
        </div>
      </div>

      {expanded && (
        <div className="p-6 bg-white text-gray-900 text-[17px] sm:text-[18px] font-normal sm:font-medium leading-[1.8] tracking-normal font-serif space-y-2">
          {content
            .split('\n')
            .map((line, i) => {
              const cleanedLine = line.replace(/^\s*-{1,2}\s*/, '• ');
              const parts = cleanedLine.split(/(\*\*.*?\*\*)/g);

              return (
                <div key={i}>
                  {parts.map((part, index) => {
                    if (part.startsWith('**') && part.endsWith('**')) {
                      return <strong key={index}>{part.slice(2, -2)}</strong>;
                    }
                    const segments = part.split(/(https?:\/\/\S+)/g);
                    return (
                      <React.Fragment key={index}>
                        {segments.map((seg, idx) =>
                          /https?:\/\//.test(seg) ? (
                            <a
                              key={idx}
                              href={seg}
                              className="text-blue-600 underline"
                              target="_blank"
                              rel="noopener noreferrer"
                            >
                              {seg}
                            </a>
                          ) : (
                            <span key={idx}>{seg}</span>
                          )
                        )}
                      </React.Fragment>
                    );
                  })}
                </div>
              );
            })}
        </div>
      )}
    </div>
  );
};

export default ReportItem;