#!/usr/bin/env node
/**
 * Context Warning - PostToolUse Hook
 * Monitors context usage and warns when it exceeds 80%
 */

const fs = require('fs')

const WARNING_THRESHOLD = 80

async function main() {
  let input = ''
  for await (const chunk of process.stdin) input += chunk

  try {
    const data = JSON.parse(input)
    const transcriptPath = data.transcript_path

    if (!transcriptPath || !fs.existsSync(transcriptPath)) {
      console.log('{}')
      return
    }

    const content = fs.readFileSync(transcriptPath, 'utf-8')
    const totalChars = content.length
    const estimatedTokens = Math.ceil(totalChars / 4)
    const CONTEXT_WINDOW = 150000
    const usagePercent = Math.round((estimatedTokens / CONTEXT_WINDOW) * 100)
    const remainingPercent = Math.max(0, 100 - usagePercent)

    if (usagePercent >= WARNING_THRESHOLD) {
      const warning = usagePercent >= 90
        ? '🚨 CRITICAL'
        : usagePercent >= 80
          ? '⚠️ WARNING'
          : ''

      console.log(JSON.stringify({
        systemMessage: `${warning} Context: ${usagePercent}% used (~${estimatedTokens} tokens). Remaining: ${remainingPercent}%`
      }))
    } else {
      console.log(JSON.stringify({
        systemMessage: `Context: ${usagePercent}% used | ${remainingPercent}% remaining`
      }))
    }
  } catch (e) {
    console.error('Context warning error:', e.message)
    console.log('{}')
  }
}

if (require.main === module) {
  main()
}
