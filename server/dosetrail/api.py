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