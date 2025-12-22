"""Read API for the dashboard."""

import os
from datetime import date

from fastapi import FastAPI, HTTPException
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from pydantic import BaseModel

app = FastAPI(title="dosetrail", version="0.5.0")
pool = ConnectionPool(os.environ.get("DATABASE_URL", "postgresql://dosetrail@localhost/dosetrail"), kwargs={"row_factory": dict_row})

