import { Card, Group, SegmentedControl, SimpleGrid, Stack, Text, Title } from '@mantine/core'
import { useState } from 'react'
import { useOverview, useProtocols } from '../api'
import { AlertList } from '../components/AlertList'
import { ProtocolChart } from '../components/ProtocolChart'

const DRL = { 'CT HEAD ROUTINE': 970, 'CT CHEST ROUTINE': 350, 'CT ABDOMEN PELVIS': 745, 'CT LUMBAR SPINE': 700 }

function Stat({ label, value, unit }: { label: string; value: string | number | undefined; unit?: string }) {
  return (
    <Card withBorder padding="md">
      <Text size="xs" c="dimmed" tt="uppercase" fw={600}>{label}</Text>
      <Text ff="monospace" fz={26} fw={500}>{value ?? '—'}{unit && <Text span size="sm" c="dimmed"> {unit}</Text>}</Text>
    </Card>
  )
}

export function Dashboard() {
  const [days, setDays] = useState('90')
  const { data: o } = useOverview()
  const { data: protocols = [] } = useProtocols(Number(days))
  return (
    <Stack gap="lg">
      <SimpleGrid cols={4}>
        <Stat label="Studies this month" value={o?.studies} />
        <Stat label="CT" value={o?.ct} />
        <Stat label="Median effective dose" value={o?.median_msv?.toFixed(1)} unit="mSv" />
        <Stat label="Open alerts" value={o?.open_alerts} />
      </SimpleGrid>
      <Card withBorder>