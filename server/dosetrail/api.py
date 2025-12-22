"""Read API for the dashboard."""

import os
from datetime import date

from fastapi import FastAPI, HTTPException
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from pydantic import BaseModel

app = FastAPI(title="dosetrail", version="0.5.0")
pool = ConnectionPool(os.environ.get("DATABASE_URL", "postgresql://dosetrail@localhost/dosetrail"), kwargs={"row_factory": dict_row})


def rows(sql: str, *params):
    with pool.connection() as conn:
        return conn.execute(sql, params).fetchall()


@app.get("/api/overview")
def overview(since: date | None = None):
    since = since or date.today().replace(day=1)
    [totals] = rows(
        """SELECT count(*) AS studies, count(*) FILTER (WHERE modality = 'CT') AS ct,
                  (SELECT count(*) FROM alerts WHERE reviewed_at IS NULL) AS open_alerts,
                  percentile_cont(0.5) WITHIN GROUP (ORDER BY effective_msv) AS median_msv
           FROM studies WHERE performed_at >= %s""",
        since,
    )
    return totals


@app.get("/api/protocols")
def protocols(modality: str = "CT", days: int = 90):
    """Per protocol: the distribution of DLP, for the box plot against the DRL line."""
    return rows(
        """SELECT protocol, count(*) AS n,
                  percentile_cont(ARRAY[0.05, 0.25, 0.5, 0.75, 0.95]) WITHIN GROUP (ORDER BY total_dlp) AS dlp
           FROM studies WHERE modality = %s AND performed_at > now() - make_interval(days => %s) AND total_dlp IS NOT NULL
           GROUP BY protocol HAVING count(*) >= 10 ORDER BY n DESC LIMIT 20""",
        modality, days,
    )
