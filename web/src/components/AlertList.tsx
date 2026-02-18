import { Badge, Button, Group, Table, Text, TextInput } from '@mantine/core'
import { useState } from 'react'
import { review, useAlerts, type Alert } from '../api'

const label: Record<Alert['kind'], { text: string; color: string }> = {
  above_drl: { text: 'Above DRL', color: 'red' },
  cumulative: { text: 'Cumulative', color: 'grape' },
  repeat_scan: { text: 'Repeat', color: 'orange' },