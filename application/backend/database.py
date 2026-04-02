"""
Database layer - MySQL for users (register/login).
"""
import os
import pymysql
from contextlib import contextmanager
from typing import Optional

# MySQL settings (read strictly from env)
# If `MYSQL_HOST` is empty/unset, the app falls back to in-memory storage.
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")


def use_mysql() -> bool:
    return bool(MYSQL_HOST and MYSQL_HOST.strip())


@contextmanager
def get_connection():
    missing: list[str] = []
    if not MYSQL_PORT:
        missing.append("MYSQL_PORT")
    if not MYSQL_USER:
        missing.append("MYSQL_USER")
    if MYSQL_PASSWORD is None:
        missing.append("MYSQL_PASSWORD")
    if not MYSQL_DATABASE:
        missing.append("MYSQL_DATABASE")
    if missing:
        raise RuntimeError(f"Missing MySQL env vars when MYSQL_HOST is set: {', '.join(missing)}")
    conn = pymysql.connect(
        host=MYSQL_HOST,
        port=int(MYSQL_PORT),
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    """Create users table if not exists (when using MySQL)."""
    if not use_mysql():
        return
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id          INT AUTO_INCREMENT PRIMARY KEY,
                    email       VARCHAR(255) NOT NULL UNIQUE,
                    password    VARCHAR(255) NOT NULL,
                    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_email (email)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)


def get_user_by_email(email: str) -> Optional[dict]:
    """Return user row {email, password} or None."""
    if not use_mysql():
        return None
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT email, password FROM users WHERE email = %s", (email,))
            return cur.fetchone()


def create_user(email: str, password_hash: str) -> None:
    """Insert a new user."""
    if not use_mysql():
        return
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (email, password) VALUES (%s, %s)",
                (email, password_hash),
            )


def user_exists(email: str) -> bool:
    """Check if email is already registered."""
    return get_user_by_email(email) is not None
