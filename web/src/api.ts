import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then(r => {