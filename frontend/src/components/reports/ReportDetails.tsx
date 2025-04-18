// ReportDetails.tsx
import React, { useEffect, useState } from 'react'
import ReportItem from './ReportItem'

interface Section {
  title: string
  content: string
  score: number
  colorClass: string
}

const sectionNames = [
  'HOME PAGE',
  'CATEGORY PAGE',
  'PRODUCT PAGE',
  'CART PAGE',
  'CHECKOUT PAGE',
  'FOOTER',
]

const defaultSections: Section[] = sectionNames.map(title => ({
  title,
  content: '',
  score: 0,
  colorClass: '',
}))

function cleanText(text: string): string {
  return text
    .replace(/\r\n/g, '\n')
    .split('\n')
    .map(line => line.trim())
    .join('\n')
}

/**
 * Parses sequential DEVICE blocks for each section,
 * capturing only lines starting with "• " and the Average Score line.
 */
function parseDynamicContent(raw: unknown) {
  let txt =
    typeof raw === 'object' && raw !== null && 'output' in raw
      ? (raw as { output: string }).output
      : raw
  if (typeof txt !== 'string') txt = String(txt)

  const lines = cleanText(txt as string).split('\n')
  const desktopMap: Record<string, string[]> = {}
  const mobileMap: Record<string, string[]> = {}
  let sectionIndex = -1
  let currentDevice: 'desktop' | 'mobile' | null = null

  for (const line of lines) {
    if (/^<!--\s*DEVICE:desktop\s*-->$/i.test(line)) {
      sectionIndex++  // move to next section
      currentDevice = 'desktop'
      const section = sectionNames[sectionIndex]
      desktopMap[section] = []
      mobileMap[section] = []
      continue
    }
    if (/^<!--\s*DEVICE:mobile\s*-->$/i.test(line)) {
      currentDevice = 'mobile'
      continue
    }

    if (sectionIndex < 0) continue

    const section = sectionNames[sectionIndex]
    const isBullet = /^•\s/.test(line)
    const isAverage = /^\*\*Average Score/.test(line)
    if (currentDevice === 'desktop' && (isBullet || isAverage)) {
      desktopMap[section].push(line)
    } else if (currentDevice === 'mobile' && (isBullet || isAverage)) {
      mobileMap[section].push(line)
    }
  }

  return {
    desktop: Object.fromEntries(
      Object.entries(desktopMap).map(([k, v]) => [k, v.join('\n').trim()])
    ),
    mobile: Object.fromEntries(
      Object.entries(mobileMap).map(([k, v]) => [k, v.join('\n').trim()])
    ),
  }
}

/**
 * Extracts the numeric score from the Average Score line.
 */
function extractPageScore(content: string): number {
  // Strip out bold markers so our regexes don’t get confused
  const plain = content.replace(/\*\*/g, '')

  // 1) Try the “Average Score (Desktop|Mobile): … → Rating” line
  const avgRegex =
    /Average Score\s*\(\s*(?:Desktop|Mobile)\)\s*:\s*[^→]*→\s*(Excellent|Good|Can Be Improved|Bad)/i
  const avgMatch = avgRegex.exec(plain)
  if (avgMatch) {
    const map = { excellent: 5, good: 4, 'can be improved': 3, bad: 2 } as const
    return map[avgMatch[1].toLowerCase() as keyof typeof map]
  }

  // 2) Fallback: look for any “Score: <number>”
  const numRegex = /Score\s*:\s*(\d+)/i
  const numMatch = numRegex.exec(plain)
  if (numMatch) {
    return parseInt(numMatch[1], 10)
  }

  return 0
}


function getColorClass(score: number): string {
  switch (score) {
    case 5:
      return 'bg-green-500'
    case 4:
      return 'bg-green-300'
    case 3:
      return 'bg-yellow-400'
    case 2:
      return 'bg-red-500'
    default:
      return 'bg-gray-300'
  }
}

interface ReportDetailsProps {
  reportText: unknown
  view: 'desktop' | 'mobile'
}

const ReportDetails: React.FC<ReportDetailsProps> = ({ reportText, view }) => {
  const [sections, setSections] = useState<Section[]>(defaultSections)

  useEffect(() => {
    const { desktop, mobile } = parseDynamicContent(reportText)
    const selected = view === 'desktop' ? desktop : mobile

    const updated = sectionNames.map(title => {
      const content = selected[title] || ''
      const score = extractPageScore(content)
      const colorClass = getColorClass(score)
      return { title, content, score, colorClass }
    })

    setSections(updated)
  }, [reportText, view])

  return (
    <div className="w-full space-y-4">
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