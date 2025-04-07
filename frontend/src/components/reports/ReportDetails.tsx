import React, { useState, useEffect } from 'react';
import ReportItem from './ReportItem';

interface Section {
  title: string;
  rating: 'green' | 'orange' | 'yellow' | 'red';
  content: string;
}

// Default sections with one-word fallback content.
const defaultSections: Section[] = [
  { title: 'HOME PAGE', rating: 'green', content: 'Home' },
  { title: 'CATEGORY PAGE', rating: 'orange', content: 'Category' },
  { title: 'PRODUCT PAGE', rating: 'yellow', content: 'Product' },
  { title: 'CHECKOUT PAGE', rating: 'red', content: 'Checkout' },
  { title: 'NAVIGATION', rating: 'orange', content: 'Navigation' },
  { title: 'SUMMARY', rating: 'orange', content: 'Summary' },
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
    'CHECKOUT PAGE',
    'NAVIGATION',
    'SUMMARY',
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
    // Detect headers: expecting lines that start with "**" and end with ":**"
    if (line.startsWith('**') && line.endsWith(':**')) {
      flushContent();
      // Extract header text between the markers.
      const headerText = line.slice(2, line.length - 3).trim();
      const upperHeader = headerText.toUpperCase();
      // Only process headers that match our valid keys.
      if (validKeys.has(upperHeader)) {
        currentKey = upperHeader;
      } else {
        currentKey = null;
      }
    } else {
      if (currentKey) {
        currentContent.push(line);
      }
    }
  }
  flushContent();
  return contentMap;
}

interface ReportDetailsProps {
  reportText: unknown;
}

const ReportDetails: React.FC<ReportDetailsProps> = ({ reportText }) => {
  const [sections, setSections] = useState<Section[]>(defaultSections);

  useEffect(() => {
    const dynamicContentMap = parseDynamicContent(reportText);
    // Update default sections with dynamic content when available.
    const updatedSections = defaultSections.map(section => {
      const key = section.title.toUpperCase();
      return dynamicContentMap[key]
        ? { ...section, content: dynamicContentMap[key] }
        : section;
    });
    setSections(updatedSections);
  }, [reportText]);

  return (
    <div className="border-t border-gray-200">
      {sections.map(section => (
        <ReportItem
          key={section.title}
          title={section.title}
          rating={section.rating}
          content={section.content}
        />
      ))}
    </div>
  );
};

export default ReportDetails;