import ReactECharts from 'echarts-for-react'
import type { ProtocolDose } from '../api'
import { doseColors } from '../theme'

/** DLP distribution per protocol as box plots (5th–95th percentile whiskers) with the DRL marked. */