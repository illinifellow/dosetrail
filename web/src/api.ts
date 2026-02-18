import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then(r => {
  if (!r.ok) throw new Error(`${r.status} ${url}`)
  return r.json()
})

export type Overview = { studies: number; ct: number; open_alerts: number; median_msv: number | null }
export type ProtocolDose = { protocol: string; n: number; dlp: [number, number, number, number, number] }
export type Alert = {
  id: number; study_uid: string; kind: 'above_drl' | 'cumulative' | 'repeat_scan'; detail: string
  raised_at: string; protocol: string | null; device: string | null; total_dlp: number | null
}
