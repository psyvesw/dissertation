import json
import re
import os
import sqlite3
from fileStreams import getFileJsonStream

# Define your keyword lists
chatgpt_keywords = [
    r"\bchatgpt\b", r"\bgpt\b", r"\bgpt-3\b", r"\bgpt-4\b", r"\bopenai\b", r"\baigc\b", r"\bllm\b",
    r"\blarge language model\b", r"\bai\b", r"\bartificial intelligence\b",
    r"\bai-generated content\b", r"\bartificial intelligence generated content\b", r"\bai chatbot\b",
    r"\bconversational ai\b", r"\btransformer model\b", r"\bgenerative model\b"
]

education_keywords = [
    r"\beducation\b", r"\blearn\b", r"\bteach\b", r"\bstudy\b", r"\bschool\b", r"\buniversity\b",
    r"\bexam\b", r"\bhomework\b", r"\bpaper\b", r"\bclass\b", r"\blecture\b", r"\bcurriculum\b", r"\bsyllabus\b",
    r"\bprofessor\b", r"\bteacher\b", r"\bstudent\b", r"\bacademic\b", r"\bscholar\b", r"\bhigher education\b",
    r"\bcollege\b", r"\bacademy\b", r"\bcourse\b", r"\blesson\b", r"\bassignment\b", r"\bdegree\b", r"\bgraduate\b",
    r"\bundergraduate\b", r"\bphd\b", r"\bthesis\b", r"\bdissertation\b", r"\bresearch\b", r"\beducational\b",
    r"\bclassroom\b", r"\binstruction\b", r"\bpedagogy\b", r"\bassessment\b", r"\bonline learning\b",
    r"\bdistance learning\b", r"\be-learning\b", r"\bvirtual learning\b", r"\bdissertation\b"
]

# Function to check if content is relevant based on keywords
def is_relevant(content, chatgpt_keywords, education_keywords):
    content = content.lower()
    contains_chatgpt = any(re.search(kw, content) for kw in chatgpt_keywords)
    contains_education = any(re.search(kw, content) for kw in education_keywords)
    return contains_chatgpt and contains_education

def post_exists(post_id, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM posts WHERE id = ?", (post_id,))
    return cursor.fetchone() is not None

def comment_exists(comment_id, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM comments WHERE id = ?", (comment_id,))
    return cursor.fetchone() is not None

def processRow(row, conn):
    data = row

    if 'title' in data:  # It's a post
        title = data.get('title', '')
        selftext = data.get('selftext', '')

        if is_relevant(title, chatgpt_keywords, education_keywords) or is_relevant(selftext, chatgpt_keywords, education_keywords):
            if not post_exists(data['id'], conn):
                print(f"Relevant post found: {data.get('id')}")
                save_post(data, conn)
            else:
                print(f"Post already exists: {data.get('id')}")
        else:
            print(f"Irrelevant post: {data.get('id')}")
    else:  # It's a comment
        body = data.get('body', '')

        if is_relevant(body, chatgpt_keywords, education_keywords):
            if not comment_exists(data['id'], conn):
                print(f"Relevant comment found: {data.get('id')}")
                save_comment(data, conn)
            else:
                print(f"Comment already exists: {data.get('id')}")
        else:
            print(f"Irrelevant comment: {data.get('id')}")

def save_post(post, conn):
    post_id = post.get('id')
    print(f"Processing post: {post_id}")
    with conn:
        conn.execute("""
            INSERT INTO posts (id, title, selftext, author, created_utc, permalink, score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (post['id'], post['title'], post['selftext'], post['author'], post['created_utc'], post['permalink'], post['score']))

def save_comment(comment, conn):
    comment_id = comment.get('id')
    print(f"Processing comment: {comment_id}")
    with conn:
        conn.execute("""
            INSERT INTO comments (id, body, author, created_utc, permalink, score, parent_id, link_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (comment['id'], comment['body'], comment['author'], comment['created_utc'], comment['permalink'], comment['score'], comment['parent_id'], comment['link_id']))

# Create a new SQLite database (or connect to an existing one)
conn = sqlite3.connect('filtered_data/relevant_data.db')

# Create tables for posts and comments
conn.execute("""
CREATE TABLE IF NOT EXISTS posts (
    id TEXT PRIMARY KEY,
    title TEXT,
    selftext TEXT,
    author TEXT,
    created_utc INTEGER,
    permalink TEXT,
    score INTEGER
)
""")
conn.execute("""
CREATE TABLE IF NOT EXISTS comments (
    id TEXT PRIMARY KEY,
    body TEXT,
    author TEXT,
    created_utc INTEGER,
    permalink TEXT,
    score INTEGER,
    parent_id TEXT,
    link_id TEXT
)
""")

# The fileOrFolderPath variable should be set to the path of your downloaded data
fileOrFolderPath = r'/Users/vesper/Desktop/LSE/Capstone Project/dissertation/data'

# Process all files in the specified folder
def process_files_in_folder(folder_path, conn):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        print(f"Processing file: {file_path}")
        json_stream = getFileJsonStream(file_path)
        if json_stream is not None:
            for _, row in json_stream:
                processRow(row, conn)
        else:
            print(f"Could not open JSON stream for file: {filename}")

# Process the files
process_files_in_folder(fileOrFolderPath, conn)

# Close the database connection
conn.close()
