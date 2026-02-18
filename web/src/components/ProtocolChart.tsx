import ReactECharts from 'echarts-for-react'
import type { ProtocolDose } from '../api'
import { doseColors } from '../theme'

/** DLP distribution per protocol as box plots (5th–95th percentile whiskers) with the DRL marked. */
export function ProtocolChart({ data, drl }: { data: ProtocolDose[]; drl: Record<string, number> }) {
  const names = data.map(d => `${d.protocol} (${d.n})`)
  return (
    <ReactECharts
      style={{ height: 36 * data.length + 60 }}
      option={{
        textStyle: { fontFamily: 'Inter' },
        grid: { left: 190, right: 30, top: 10, bottom: 30 },