import { Badge, Button, Group, Table, Text, TextInput } from '@mantine/core'
import { useState } from 'react'
import { review, useAlerts, type Alert } from '../api'

const label: Record<Alert['kind'], { text: string; color: string }> = {
  above_drl: { text: 'Above DRL', color: 'red' },
  cumulative: { text: 'Cumulative', color: 'grape' },
  repeat_scan: { text: 'Repeat', color: 'orange' },
}

export function AlertList() {
  const { data = [], mutate } = useAlerts()
  const [note, setNote] = useState<Record<number, string>>({})
  return (
    <Table verticalSpacing="xs" highlightOnHover>
      <Table.Thead>
        <Table.Tr><Table.Th>When</Table.Th><Table.Th>Why</Table.Th><Table.Th>Protocol</Table.Th><Table.Th>Scanner</Table.Th><Table.Th /></Table.Tr>
      </Table.Thead>