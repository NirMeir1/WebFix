import React, { useState, useEffect } from 'react'
import ReportItem from './ReportItem'

interface PageViewData {
  criteria: Array<{
    criterion: string
    finding: string
    score: number
    why_it_matters: string
    why_this_score: string
    how_to_improve: string
  }>
  average_score: number
  label: string
  recommendations: string[]
}

export interface ReportSchema {
  pages: Record<
    | 'home'
    | 'category'
    | 'product'
    | 'cart'
    | 'checkout'
    | 'footer'
    // Deep-only sections
    | 'general'
    | 'navigation'
    | 'search'
    | 'cart_widget',
    { desktop: PageViewData; mobile: PageViewData }
  >
}

interface DisplaySection {
  title: string
  content: string
  score: number
  colorClass: string
}

interface ReportDetailsProps {
  report: ReportSchema
  view: 'desktop' | 'mobile'
  isCached?: boolean
  reportType: 'basic' | 'deep'
}

const pageOrder: { key: keyof ReportSchema['pages']; title: string }[] = [
  { key: 'home', title: 'HOME PAGE' },
  { key: 'category', title: 'CATEGORY PAGE' },
  { key: 'product', title: 'PRODUCT PAGE' },
  { key: 'cart', title: 'CART PAGE' },
  { key: 'checkout', title: 'CHECKOUT PAGE' },
  { key: 'footer', title: 'FOOTER' },
]

// Extra sections for deep reports
const deepPageOrder: { key: keyof ReportSchema['pages']; title: string }[] = [
  { key: 'general', title: 'GENERAL' },
  { key: 'navigation', title: 'NAVIGATION' },
  { key: 'search', title: 'SEARCH' },
  { key: 'cart_widget', title: 'CART WIDGET' },
]

const labelColorMap: Record<string, string> = {
  Excellent: 'bg-green-500',
  Good: 'bg-green-300',
  'Can Be Improved': 'bg-yellow-400',
  Bad: 'bg-red-500',
}

const ReportDetails: React.FC<ReportDetailsProps> = ({ report, view, isCached = false, reportType }) => {
  const [sections, setSections] = useState<DisplaySection[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    try {
      const device = view.toLowerCase() as 'desktop' | 'mobile'

      // Helper to build a section or skip if missing
      const buildSection = (
        key: keyof ReportSchema['pages'],
        title: string
      ): DisplaySection | null => {
        const pageData = report.pages[key]?.[device]
        if (!pageData) {
          // Skip missing section
          return null
        }

        // Criteria lines
        const criteriaLines = pageData.criteria.map(c =>
          `• **${c.criterion}:** ${c.finding} (Score: ${c.score})\n` +
          `    – *Why it matters:* ${c.why_it_matters}\n` +
          `    – *Why this score:* ${c.why_this_score}\n` +
          `    – *How to improve:* ${c.how_to_improve}`
        );

        // Average score line
        const avgLine =
          `**Average Score (${device.charAt(0).toUpperCase() + device.slice(1)}):** ${pageData.average_score} → ${pageData.label}`

        // Recommendations lines
        const recLines = pageData.recommendations.map(r => `• ${r}`)

        const parts: string[] = []
        parts.push(['**Explanation –**', ...criteriaLines].join('\n'))
        parts.push(avgLine)
        if (recLines.length) {
          parts.push(['**Recommendations –**', ...recLines].join('\n'))
        }

        return {
          title,
          content: parts.join('\n\n'),
          score: pageData.average_score,
          colorClass: labelColorMap[pageData.label] || 'bg-gray-300',
        }
      }

      // Build and filter base sections
      const baseSections = pageOrder
        .map(({ key, title }) => buildSection(key, title))
        .filter((s): s is DisplaySection => s !== null)

      // Build and filter deep-only sections if needed
      const deepSections = reportType === 'deep'
        ? deepPageOrder
            .map(({ key, title }) => buildSection(key, title))
            .filter((s): s is DisplaySection => s !== null)
        : []

      setSections(
        reportType === 'deep'
          ? [...deepSections, ...baseSections]
          : [...baseSections]
      )
      setError(null)
    } catch (e) {
      console.error('Unexpected error processing report data', e)
      setSections([])
      setError('Failed to load report data.')
    }
  }, [report, view, reportType])

  if (error) {
    return <div className="text-red-500">{error}</div>
  }

  if (sections.length === 0) {
    return <div>No report data available.</div>
  }

  return (
    <div className="w-full space-y-4">
      {isCached && (
        <div className="bg-yellow-200 p-4 rounded-md text-center text-lg leading-relaxed">
          Hi there!
          Since you’ve already generated this report within the past 7 days,
          we’re presenting it to you again without re-testing the live data.
          We recommend waiting at least 7 days
          for meaningful changes to take effect before running a new report.
          Thanks for your understanding! 😊
        </div>
      )}

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
  )
}

export default ReportDetails