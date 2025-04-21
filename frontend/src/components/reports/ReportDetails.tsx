import React, { useState, useEffect } from 'react'
import ReportItem from './ReportItem'

interface PageViewData {
  criteria: Array<{
    criterion: string
    finding: string
    score: number
  }>
  average_score: number
  label: string
  recommendations: string[]
}

export interface ReportSchema {
  pages: Record<
    'home' | 'category' | 'product' | 'cart' | 'checkout' | 'footer',
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
}

const pageOrder: { key: keyof ReportSchema['pages']; title: string }[] = [
  { key: 'home', title: 'HOME PAGE' },
  { key: 'category', title: 'CATEGORY PAGE' },
  { key: 'product', title: 'PRODUCT PAGE' },
  { key: 'cart', title: 'CART PAGE' },
  { key: 'checkout', title: 'CHECKOUT PAGE' },
  { key: 'footer', title: 'FOOTER' },
]

const labelColorMap: Record<string, string> = {
  Excellent: 'bg-green-500',
  Good: 'bg-green-300',
  'Can Be Improved': 'bg-yellow-400',
  Bad: 'bg-red-500',
}

const ReportDetails: React.FC<ReportDetailsProps> = ({ report, view, isCached = false }) => {
  const [sections, setSections] = useState<DisplaySection[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    try {
      // Ensure view is lower-case
      const device = view.toLowerCase() as 'desktop' | 'mobile'

      const newSections: DisplaySection[] = pageOrder.map(({ key, title }) => {
        const pageData = report.pages[key]?.[device]
        if (!pageData) {
          throw new Error(`Missing data for page “${key}” (${device})`)
        }

        // Build markdown lines for criteria
        const criteriaLines = pageData.criteria.map(
          c => `• **${c.criterion}:** ${c.finding} (Score: ${c.score})`
        )

        // Average score and label
        const avgLine =
          `**Average Score (${device.charAt(0).toUpperCase() + device.slice(1)}):** ` +
          `${pageData.average_score} → ${pageData.label}`

        // Recommendations
        const recLines = pageData.recommendations.map(r => `• ${r}`)

        // Compose full content
        const parts: string[] = []
        parts.push(
          ['**Explanation –**', ...criteriaLines].join('\n')
        )
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
      })

      setSections(newSections)
      setError(null)
    } catch (e) {
      console.error('Failed to process report data', e)
      setSections([])
      setError('Failed to load report data.')
    }
  }, [report, view])

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