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
        tooltip: { trigger: 'item' },
        xAxis: { type: 'value', name: 'DLP, mGy·cm', nameLocation: 'middle', nameGap: 22, splitLine: { lineStyle: { color: '#e3e1db' } } },
        yAxis: { type: 'category', data: names, inverse: true, axisTick: { show: false } },
        series: [
          {
            type: 'boxplot',
            data: data.map(d => d.dlp),
            itemStyle: { color: '#e8f0ff', borderColor: '#1365fc' },
          },
          {
            type: 'scatter',
            symbol: 'rect',
            symbolSize: [3, 22],