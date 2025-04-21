import logging
import sqlite3
from datetime import datetime
from piersfan import config
from piersfan.config import Config

_logger = logging.getLogger(__name__)


class JobStatus:
    def __init__(self, db_name=config.ChokaDB):
        self.db_path = Config.get_db_path(db_name)
        self._table_initialized = False

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _ensure_table_initialized(self):
        if not self._table_initialized:
            self._initial_table()
            self._table_initialized = True

    def _initial_table(self):
        with self._get_connection() as conn:
            conn.execute(
                """  
                CREATE TABLE IF NOT EXISTS job_status (  
                    job_name TEXT PRIMARY KEY,  
                    executed_at TEXT NOT NULL  
                );  
            """
            )

    def get_last_execution_time(self, job_name="default_job"):
        self._ensure_table_initialized()
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """  
                SELECT executed_at FROM job_status  
                WHERE job_name = ?  
            """,
                (job_name,),
            )
            row = cur.fetchone()
        return row[0] if row else None

    def save_execution_time(self, job_name="default_job"):
        self._ensure_table_initialized()
        now = datetime.utcnow().isoformat()
        with self._get_connection() as conn:
            conn.execute(
                """  
                INSERT INTO job_status (job_name, executed_at)  
                VALUES (?, ?)  
                ON CONFLICT(job_name) DO UPDATE SET executed_at=excluded.executed_at  
            """,
                (job_name, now),
            )

    def show_job_status(self):
        self._ensure_table_initialized()
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT job_name, executed_at FROM job_status")
            rows = cur.fetchall()
        if not rows:
            print("No job status found.")
        else:
            for row in rows:
                print(f"Job: {row[0]}, Last Executed At: {row[1]}")
