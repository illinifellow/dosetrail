import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then(r => {
  if (!r.ok) throw new Error(`${r.status} ${url}`)
  return r.json()
})

export type Overview = { studies: number; ct: number; open_alerts: number; median_msv: number | null }