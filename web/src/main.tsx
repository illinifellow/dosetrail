import '@mantine/core/styles.css'
import { AppShell, Group, MantineProvider, Title } from '@mantine/core'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Dashboard } from './pages/Dashboard'
import { theme } from './theme'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <MantineProvider theme={theme} defaultColorScheme="auto">
      <AppShell header={{ height: 48 }} padding="lg">
        <AppShell.Header><Group h="100%" px="lg"><Title order={3}>dosetrail</Title></Group></AppShell.Header>
        <AppShell.Main><Dashboard /></AppShell.Main>
      </AppShell>
    </MantineProvider>
  </StrictMode>,
)