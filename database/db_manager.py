import sqlite3
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class DatabaseManager:
    """Manages SQLite database for DevDocs application."""

    def __init__(self, db_path: str = "devdocs.db"):
        """Initialize database manager with given path."""
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """Create database tables if they don't exist."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Topics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                github_url TEXT NOT NULL,
                local_path TEXT NOT NULL,
                subfolder TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Documents table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                relative_path TEXT NOT NULL,
                is_read INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
            )
        """)

        conn.commit()
        conn.close()

    def add_topic(self, name: str, github_url: str, local_path: str, subfolder: Optional[str] = None):
        """Add a new documentation topic."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO topics (name, github_url, local_path, subfolder)
                VALUES (?, ?, ?, ?)
            """, (name, github_url, local_path, subfolder))
            conn.commit()
            topic_id = cursor.lastrowid
            return topic_id
        finally:
            conn.close()

    def get_all_topics(self):
        """Get all topics."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM topics ORDER BY name")
        topics = cursor.fetchall()
        conn.close()
        return topics

    def get_topic(self, topic_id: int):
        """Get a specific topic."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM topics WHERE id = ?", (topic_id,))
        topic = cursor.fetchone()
        conn.close()
        return topic

    def delete_topic(self, topic_id: int):
        """Delete a topic and its documents."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM topics WHERE id = ?", (topic_id,))
        conn.commit()
        conn.close()

    def add_document(self, topic_id: int, title: str, filename: str, file_path: str, relative_path: str):
        """Add a new document."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO documents (topic_id, title, filename, file_path, relative_path)
                VALUES (?, ?, ?, ?, ?)
            """, (topic_id, title, filename, file_path, relative_path))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def get_topic_documents(self, topic_id: int):
        """Get all documents for a topic."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM documents 
            WHERE topic_id = ? 
            ORDER BY relative_path
        """, (topic_id,))
        documents = cursor.fetchall()
        conn.close()
        return documents

    def get_document(self, doc_id: int):
        """Get a specific document."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
        doc = cursor.fetchone()
        conn.close()
        return doc

    def mark_as_read(self, doc_id: int, is_read: int = 1):
        """Mark document as read/unread."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE documents 
            SET is_read = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (is_read, doc_id))
        conn.commit()
        conn.close()

    def get_unread_count(self, topic_id: int):
        """Get count of unread documents for a topic."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as count FROM documents 
            WHERE topic_id = ? AND is_read = 0
        """, (topic_id,))
        result = cursor.fetchone()
        conn.close()
        return result['count']

    def clear_documents_for_topic(self, topic_id: int):
        """Clear all documents for a topic (used before re-downloading)."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM documents WHERE topic_id = ?", (topic_id,))
        conn.commit()
        conn.close()

    def update_topic_timestamp(self, topic_id: int):
        """Update topic's last update timestamp."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE topics 
            SET updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (topic_id,))
        conn.commit()
        conn.close()
