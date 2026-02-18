import { Badge, Button, Group, Table, Text, TextInput } from '@mantine/core'
import { useState } from 'react'
import { review, useAlerts, type Alert } from '../api'

const label: Record<Alert['kind'], { text: string; color: string }> = {