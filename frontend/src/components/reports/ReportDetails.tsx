import React, { useEffect, useState } from 'react';
import ReportItem from './ReportItem';

interface Section {
  title: string;
  content: string;
  score: number;
  colorClass: string;
}

const sectionNames = [
  'HOME PAGE',
  'CATEGORY PAGE',
  'PRODUCT PAGE',
  'CART PAGE',
  'CHECKOUT PAGE',
  'THANK YOU PAGE',
];

const defaultSections: Section[] = sectionNames.map(title => ({
  title,
  content: '',
  score: 0,
  colorClass: '',
}));

function cleanText(text: string): string {
  return text
    .replace(/\r\n/g, '\n')
    .split('\n')
    .map(line => line.trim())
    .join('\n');
}

function parseDynamicContent(rawText: unknown): {
  desktop: { [key: string]: string };
  mobile: { [key: string]: string };
} {
  let text = typeof rawText === 'object' && rawText !== null && 'output' in rawText
    ? (rawText as { output: string }).output
    : rawText;

  if (typeof text !== 'string') text = String(text);
  const lines = cleanText(String(text)).split('\n');

  const desktop: { [key: string]: string } = {};
  const mobile: { [key: string]: string } = {};

  let currentKey: string | null = null;
  let targetMap = desktop;
  let currentContent: string[] = [];

  function flush() {
    if (currentKey && currentContent.length) {
      targetMap[currentKey] = currentContent.join('\n').trim();
    }
    currentContent = [];
  }

  for (const line of lines) {
    const match = line.match(/\*\*(.+?):\s*(Desktop|Mobile)\*\*/i);
    if (match) {
      flush();
      const section = match[1].toUpperCase();
      const platform = match[2].toLowerCase();
      currentKey = section;
      targetMap = platform === 'desktop' ? desktop : mobile;
    } else if (currentKey) {
      currentContent.push(line);
    }
  }

  flush();
  return { desktop, mobile };
}

function extractRating(content: string): number {
  const map: { [key: string]: number } = {
    'excellent': 5,
    'good': 4,
    'can be improved': 3,
    'bad': 2,
  };

  const ratingLine = content
    .split('\n')
    .find(line => line.toLowerCase().startsWith('**rating:'));

  if (ratingLine) {
    const match = ratingLine.match(/\*\*Rating:\s*([a-zA-Z\s]+)(?:\s*\((.*?)\))?\*\*/i);
    if (match) {
      const label = match[1].toLowerCase().trim(); // e.g., "good"
      return map[label] || 0;
    }
  }

  return 0;
}

function getColorClass(score: number): string {
  switch (score) {
    case 5: return 'bg-green-500';   // Excellent
    case 4: return 'bg-orange-500';  // Good
    case 3: return 'bg-yellow-400';  // Can be Improved
    case 2: return 'bg-red-500';     // Bad
    default: return 'bg-gray-300';
  }
}

interface ReportDetailsProps {
  reportText: unknown;
  view: 'desktop' | 'mobile';
}

const ReportDetails: React.FC<ReportDetailsProps> = ({ reportText, view }) => {
  const [sections, setSections] = useState<Section[]>(defaultSections);

  useEffect(() => {
    const { desktop, mobile } = parseDynamicContent(reportText);
    const selectedMap = view === 'desktop' ? desktop : mobile;

    const updatedSections = sectionNames.map(title => {
      const content = selectedMap[title] || '';
      const score = extractRating(content);
      const colorClass = getColorClass(score);
      return { title, content, score, colorClass };
    });

    setSections(updatedSections);
  }, [reportText, view]);

  return (
    <div className="w-full">
      {sections.map(section => (
        <ReportItem
          key={section.title}
          title={section.title}
          content={section.content}
          score={section.score}
          colorClass={section.colorClass}
        />
      ))}
    </div>
  );
};

export default ReportDetails;