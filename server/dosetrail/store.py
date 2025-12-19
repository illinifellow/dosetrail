"""Writes a parsed report and its alerts in one transaction. Plain SQL through psycopg: the
queries are few, and the dashboard's percentile and window queries read better as SQL than as ORM."""

import hashlib
import hmac
import os

from psycopg import Connection