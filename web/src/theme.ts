import { createTheme, type MantineColorsTuple } from '@mantine/core'

// Warm neutral surfaces and one strong blue accent, with titles in Raleway and figures in a
// monospaced face so columns of doses line up.
const accent: MantineColorsTuple = ['#e8f0ff', '#cfdfff', '#9ebdff', '#6a99fe', '#3f7bfd', '#2468fc', '#1365fc', '#0553e2', '#004acb', '#003fb3']
const warm: MantineColorsTuple = ['#fdfbf6', '#f7f5ef', '#eeebe4', '#e0ddd5', '#cfcbc2', '#aaa69c', '#827e75', '#5a5750', '#3a3733', '#262320']

export const theme = createTheme({
  primaryColor: 'accent',
  colors: { accent, warm },
  fontFamily: 'Inter, Helvetica, Arial, sans-serif',
  fontFamilyMonospace: '"Martian Mono", ui-monospace, monospace',
  headings: { fontFamily: 'Raleway, Helvetica, Arial, sans-serif', fontWeight: '600' },
  defaultRadius: 'sm',