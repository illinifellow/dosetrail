import '@mantine/core/styles.css'
import { AppShell, Group, MantineProvider, Title } from '@mantine/core'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Dashboard } from './pages/Dashboard'
import { theme } from './theme'

createRoot(document.getElementById('root')!).render(