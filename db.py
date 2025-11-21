import os
import sqlite3
import json
from datetime import datetime


DB_PATH = os.path.join(os.path.dirname(__file__), "..", "analysis.db")


def _get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    """Create tables if they do not exist."""
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS apps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            package_name TEXT UNIQUE,
            developer TEXT,
            app_type TEXT,
            risk_score INTEGER,
            risk_level TEXT,
            is_fake INTEGER,
            flagged_malicious INTEGER,
            created_at TEXT,
            evidence_json TEXT
        )
        """
    )

    conn.commit()
    conn.close()


def save_analysis(package_name, developer, app_type, risk_score, risk_level, is_fake, checks):
    """
    Save or update an analysis result for a package.

    Args:
        package_name: Android package name
        developer: Developer name from Play Store (or None)
        app_type: Simple string classification (e.g. "Fake Loan App")
        risk_score: Total risk score (0-100)
        risk_level: LOW / MEDIUM / HIGH
        is_fake: True/False if app crossed fake threshold
        checks: Full checks dict (permissions, similarity, playstore...)
    """
    conn = _get_connection()
    cursor = conn.cursor()

    now = datetime.utcnow().isoformat()
    flagged_malicious = 1 if is_fake else 0
    evidence_json = json.dumps(checks or {})

    cursor.execute(
        """
        INSERT INTO apps (
            package_name, developer, app_type, risk_score,
            risk_level, is_fake, flagged_malicious, created_at, evidence_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(package_name) DO UPDATE SET
            developer=excluded.developer,
            app_type=excluded.app_type,
            risk_score=excluded.risk_score,
            risk_level=excluded.risk_level,
            is_fake=excluded.is_fake,
            flagged_malicious=excluded.flagged_malicious,
            created_at=excluded.created_at,
            evidence_json=excluded.evidence_json
        """,
        (
            package_name,
            developer,
            app_type,
            int(risk_score),
            risk_level,
            1 if is_fake else 0,
            flagged_malicious,
            now,
            evidence_json,
        ),
    )

    conn.commit()
    conn.close()


def get_app(package_name):
    """Return a single app row (dict) if it exists, else None."""
    conn = _get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM apps WHERE package_name = ?", (package_name,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return dict(row)


def get_recent_analyses(limit=10):
    """Return the most recent analyses (simple summary only)."""
    conn = _get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT package_name, developer, app_type,
               risk_score, risk_level, is_fake,
               flagged_malicious, created_at
        FROM apps
        ORDER BY datetime(created_at) DESC
        LIMIT ?
        """,
        (limit,),
    )

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_developer_stats(developer):
    """Return basic statistics for a developer."""
    if not developer:
        return {"total_apps": 0, "malicious_apps": 0}

    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*), SUM(is_fake) FROM apps WHERE developer = ?", (developer,))
    total, malicious = cursor.fetchone()
    conn.close()

    return {
        "total_apps": total or 0,
        "malicious_apps": malicious or 0,
    }


