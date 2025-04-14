import React, { useState, useEffect } from 'react';
import ReportItem from './ReportItem';

interface Section {
  title: string;
  content: string;
  score: number;
  colorClass: string;
}

// Default sections with one-word fallback content.
const defaultSections: Section[] = [
  { title: 'HOME PAGE', content: 'Home', score: 0, colorClass: '' },
  { title: 'CATEGORY PAGE', content: 'Category', score: 0, colorClass: '' },
  { title: 'PRODUCT PAGE', content: 'Product', score: 0, colorClass: '' },
  { title: 'CART PAGE', content: 'Cart', score: 0, colorClass: '' },
  { title: 'CHECKOUT PAGE', content: 'Checkout', score: 0, colorClass: '' },
  { title: 'THANK YOU PAGE', content: 'Thanks', score: 0, colorClass: '' },
];

// Clean the text by normalizing newlines and trimming each line.
function cleanText(text: string): string {
  // Replace CRLF with LF.
  let cleaned = text.replace(/\r\n/g, '\n');
  // Trim each line.
  cleaned = cleaned
    .split('\n')
    .map(line => line.trim())
    .join('\n');
  return cleaned;
}

// Parse dynamic content from cleaned report text line by line.
function parseDynamicContent(rawText: unknown): { [key: string]: string } {
  // If rawText is an object with an "output" property, use that.
  let text = (typeof rawText === 'object' && rawText !== null && 'output' in rawText) ? (rawText as { output: string }).output : rawText;
  // Ensure text is a string.
  if (typeof text !== 'string') {
    text = String(text);
  }
  text = cleanText(text as string);
  
  const lines = (text as string).split('\n');
  const contentMap: { [key: string]: string } = {};

  // Only update sections we care about.
  const validKeys = new Set([
    'HOME PAGE',
    'CATEGORY PAGE',
    'PRODUCT PAGE',
    'CART PAGE',
    'CHECKOUT PAGE',
    'THANK YOU PAGE',
  ]);

  let currentKey: string | null = null;
  let currentContent: string[] = [];

  // Helper function to flush accumulated content.
  function flushContent() {
    if (currentKey && currentContent.length > 0) {
      contentMap[currentKey] = currentContent.join('\n').trim();
    }
    currentContent = [];
  }

  for (const line of lines) {
    const normalizedLine = line.toUpperCase().replace(/[^A-Z\s]/g, '').trim();
    const matchedKey = Array.from(validKeys).find(key => normalizedLine.includes(key));
    
    if (matchedKey) {
      flushContent();
      currentKey = matchedKey;
    } else if (currentKey) {
      currentContent.push(line);
    }
  }
  
  flushContent();
  return contentMap;
}

function extractRatings(content: string): number[] {
  const map: { [key: string]: number } = {
    'excellent': 95,
    'good': 77,
    'can be improved': 62,
    'bad': 40
  };

  const ratings: number[] = [];
  for (const [label, score] of Object.entries(map)) {
    const regex = new RegExp(label, 'gi');
    const matches = content.match(regex);
    if (matches) {
      ratings.push(...Array(matches.length).fill(score));
    }
  }

  return ratings;
};

function getColorClass(score: number): string {
  if (score >= 85) return 'bg-green-400';
  if (score >= 70) return 'bg-blue-400';
  if (score >= 55) return 'bg-yellow-400';
  return 'bg-red-500';
}

interface ReportDetailsProps {
  reportText: unknown;
}

const ReportDetails: React.FC<ReportDetailsProps> = ({ reportText }) => {
  const [sections, setSections] = useState<Section[]>([]);

  useEffect(() => {
    const dynamicContentMap = parseDynamicContent(reportText);
    const updatedSections = defaultSections.map(section => {
      const content = dynamicContentMap[section.title.toUpperCase()] || section.content;
      const ratings = extractRatings(content);
      const score = ratings.length ? Math.round(ratings.reduce((a, b) => a + b, 0) / ratings.length) : 0;
      const colorClass = getColorClass(score);
      return { ...section, content, score, colorClass };
    });
    setSections(updatedSections);
  }, [reportText]);

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