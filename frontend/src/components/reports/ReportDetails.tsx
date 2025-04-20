import React, { useMemo } from 'react'
import ReportItem from './ReportItem'

const sectionNames = [
  'HOME PAGE',
  'CATEGORY PAGE',
  'PRODUCT PAGE',
  'CART PAGE',
  'CHECKOUT PAGE',
  'FOOTER',
]

/**
 * Parses raw report text into structured content per section and device.
 */
function parseSections(raw: unknown) {
  const text =
    typeof raw === 'object' && raw !== null && 'output' in raw
      ? (raw as { output: string }).output
      : String(raw)

  const lines = text.replace(/\r\n/g, '\n').split('\n').map(l => l.trim())
  const results = sectionNames.map(() => ({ desktop: [] as string[], mobile: [] as string[] }))

  let sectionIndex = -1
  let device: 'desktop' | 'mobile' | null = null
  const deviceRegex = /^<!--\s*DEVICE:(desktop|mobile)\s*-->$/i

  for (const line of lines) {
    const match = deviceRegex.exec(line)
    if (match) {
      const dev = match[1].toLowerCase() as 'desktop' | 'mobile'
      if (dev === 'desktop') sectionIndex++
      device = dev
      continue
    }
    if (device && sectionIndex >= 0 && sectionIndex < results.length) {
      results[sectionIndex][device].push(line)
    }
  }

  return sectionNames.reduce(
    (acc, title, idx) => {
      const { desktop, mobile } = results[idx]
      ;['desktop', 'mobile'].forEach(d => {
        const lines = (d === 'desktop' ? desktop : mobile) as string[]
        const recIdx = lines.findIndex(l =>
                    /^(?:\*\*)?Recommendations\s*[:–-]/i.test(l))
        const expIdx = lines.findIndex(l =>
                    /^(?:\*\*)?Explanation\s*[:–-]/i.test(l))

        const expStart = expIdx >= 0 ? expIdx + 1 : 0
        const expEnd = recIdx >= 0 ? recIdx : lines.length

        const expLines = lines.slice(expStart, expEnd).filter(l => /^[•-]\s/.test(l) || /Average Score/.test(l))
        const recLines = recIdx >= 0 ? lines.slice(recIdx + 1).filter(l => /^[•-]\s/.test(l)) : []

        const parts: string[] = []
        if (expLines.length) parts.push(['**Explanation –**', ...expLines].join('\n'))
        if (recLines.length) parts.push(['**Recommendations –**', ...recLines].join('\n'))

        acc[d as 'desktop' | 'mobile'][title] = parts.join('\n\n').trim()
      })
      return acc
    },
    { desktop: {} as Record<string, string>, mobile: {} as Record<string, string> }
  )
}

/**
 * Extracts numeric score from content.
 */
function extractScore(content: string): number {
  const clean = content.replace(/\*\*/g, '')
  const avg = /Average Score\s*\(\s*(?:Desktop|Mobile)\)\s*:[^→]*→\s*(Excellent|Good|Can Be Improved|Bad)/i.exec(clean)
  if (avg) {
    const map = { excellent: 5, good: 4, 'can be improved': 3, bad: 2 } as const
    return map[avg[1].toLowerCase() as keyof typeof map]
  }
  const num = /Score\s*:\s*(\d+)/i.exec(clean)
  return num ? parseInt(num[1], 10) : 0
}

/**
 * Maps score to a color CSS class.
 */
function getColorClass(score: number): string {
  if (score >= 5) return 'bg-green-500'
  if (score === 4) return 'bg-green-300'
  if (score === 3) return 'bg-yellow-400'
  if (score === 2) return 'bg-red-500'
  return 'bg-gray-300'
}

interface ReportDetailsProps {
  reportText: unknown
  view: 'desktop' | 'mobile'
  isCached?: boolean
}

/**
 * Renders parsed report sections based on selected view.
 */
const ReportDetails: React.FC<ReportDetailsProps> = ({ reportText, view, isCached = false }) => {
  console.log('🔍 isCached prop =', isCached)
  const sections = useMemo(() => {
    const { desktop, mobile } = parseSections(reportText)
    const source = view === 'desktop' ? desktop : mobile
    return sectionNames.map(title => {
      const content = source[title] || ''
      const score = extractScore(content)
      return { title, content, score, colorClass: getColorClass(score) }
    })
  }, [reportText, view])

  return (
    <div className="w-full space-y-4">

      {/* Display cache message if data is cached */}
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

      {sections.map(({ title, content, score, colorClass }) => (
        <ReportItem
          key={title}
          title={title}
          content={content}
          score={score}
          colorClass={colorClass}
        />
      ))}
    </div>
  )
}

export default ReportDetails