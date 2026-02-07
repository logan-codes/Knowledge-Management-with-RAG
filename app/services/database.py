import sqlite3
from dotenv import load_dotenv
import os

class Database:
    def __init__(self):
        load_dotenv()
        self.db_path = os.path.join(os.getenv("DATA_DIR"),"sqlite_db/sqlite.db")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    path TEXT NOT NULL,
                    status VARCHAR(20) NOT NULL
                              CHECK(status IN ('uploaded', 'ingested')),
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    def add_document(self, filename, path, status="uploaded"):
        with self.conn:
            self.conn.execute("""
                INSERT INTO documents (filename, path, status) VALUES (?, ?, ?)
            """, (filename, path, status))

    def update_document_status(self, path, status):
        with self.conn:
            self.conn.execute("""
                UPDATE documents SET status = ? WHERE path = ?
            """, (status, path))
    
    def list_documents(self):
        with self.conn:
            cursor = self.conn.execute("""
                SELECT filename, status, timestamp, path FROM documents ORDER BY timestamp DESC
            """)
            return cursor.fetchall()
        
    def delete_document(self, path):
        with self.conn:
            self.conn.execute("""
                DELETE FROM documents WHERE path = ?
            """, (path,))
    
    def disconnect(self):
        self.conn.close()
    

if __name__ == "__main__":
    db = Database()
    # db.create_tables()
    # db.add_document("sample.pdf", "data/uploads/sample.pdf")
    # print(db.list_documents())
    # db.update_document_status("sample.pdf", "ingested")
    # print(db.list_documents())
    db.delete_document("sample.pdf")
    print(db.list_documents())