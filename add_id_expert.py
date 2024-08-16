import sqlite3

# Connect to the SQLite database
db_path = "/Users/vesper/Desktop/LSE/Capstone Project/dissertation/arctic_shift/filtered_data/relevant_data.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create a new table with the id column
cursor.execute("""
CREATE TABLE IF NOT EXISTS chunked_expert_data_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_id INTEGER,
    source TEXT,
    title TEXT,
    author TEXT,
    publication_date TEXT,
    content TEXT,
    chunk_id INTEGER
)
""")

# Copy data from the old table to the new table
cursor.execute("""
INSERT INTO chunked_expert_data_new (original_id, source, title, author, publication_date, content, chunk_id)
SELECT original_id, source, title, author, publication_date, content, chunk_id FROM chunked_expert_data
""")

# Drop the old table
cursor.execute("DROP TABLE chunked_expert_data")

# Rename the new table to the old table name
cursor.execute("ALTER TABLE chunked_expert_data_new RENAME TO chunked_expert_data")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Added 'id' column to 'chunked_expert_data' table.")
