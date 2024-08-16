import sqlite3
import pandas as pd
import re

# Define the is_relevant function with pre-compiled regex patterns
def is_relevant(content, chatgpt_patterns, education_patterns, exclude_patterns=None, negative_context_patterns=None):
    content = content.lower()
    contains_chatgpt = any(pattern.search(content) for pattern in chatgpt_patterns)
    contains_education = any(pattern.search(content) for pattern in education_patterns)
    contains_excluded = any(pattern.search(content) for pattern in exclude_patterns) if exclude_patterns else False
    contains_negative_context = any(pattern.search(content) for pattern in negative_context_patterns) if negative_context_patterns else False

    return contains_chatgpt and contains_education and not contains_excluded and not contains_negative_context

# Define and compile regex patterns
education_keywords = [
    r"\beducation(s)?\b", r"\blearn(ing)?\b", r"\bteach(ing)?\b", r"\bstudy(ies)?\b", r"\bschool(s)?\b", r"\buniversity(ies)?\b",
    r"\bexam(s)?\b", r"\bhomework(s)?\b", r"\bpaper(s)?\b", r"\bclass(es)?\b", r"\blecture(s)?\b", r"\bcurriculum(s)?\b", r"\bsyllabus(es)?\b",
    r"\bprofessor(s)?\b", r"\bteacher(s)?\b", r"\bstudent(s)?\b", r"\blearner(s)?\b", r"\bacademic(s)?\b", r"\bscholar(s)?\b", r"\bhigher education(s)?\b",
    r"\bcollege(s)?\b", r"\bacademy(ies)?\b", r"\bcourse(s)?\b", r"\bcoursework\b", r"\bdegree program(s)?\b", r"\bacademic degree(s)?\b",
    r"\blesson(s)?\b", r"\bassignment(s)?\b", r"\bphd(s)?\b", r"\bthesis(es)?\b", r"\bdissertation(s)?\b", r"\bresearch(es)?\b", r"\beducational(s)?\b",
    r"\bclassroom(s)?\b", r"\bpedagogy(ies)?\b", r"\bassessment(s)?\b", r"\bteaching methods?\b", r"\blearning methods?\b"
]

chatgpt_keywords = [
    r"\bchatgpt\b", r"\bgpt\b", r"\bgpt-3\b", r"\bgpt-4\b", r"\bopenai\b", r"\baigc\b", r"\bllm(s)?\b",
    r"\blarge language model(s)?\b", r"\bai\b", r"\bartificial intelligence(s)?\b",
    r"\bai-generated content\b", r"\bartificial intelligence generated content\b", r"\bai chatbot(s)?\b"
]

exclude_non_educational_ai = [
    r"\bmidjourney\b", r"\bdall-e\b", r"\bstable diffusion\b", r"\bmusic(s)?\b", r"\bgraph(s)?\b", r"\bimage(s)?\b", r"\bphoto(s)?\b", r"\bvideo(s)?\b"
]

# Negative context keywords for ambiguous terms
negative_context_keywords = [
    r"\bdegree of\b", r"\bcourse of\b", r"\bdegree to which\b", r"\bcourse of action\b", r"\bclass of\b", 
    r"\blife lesson\b"
]

# Compile the regex patterns for performance
education_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in education_keywords]
chatgpt_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in chatgpt_keywords]
exclude_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in exclude_non_educational_ai]
negative_context_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in negative_context_keywords]

# Connect to the SQLite database
db_path = "/Users/vesper/Desktop/LSE/Capstone Project/dissertation/arctic_shift/filtered_data/relevant_data.db"
conn = sqlite3.connect(db_path)

# Load the cleaned public dataset
public_data = pd.read_sql_query("SELECT * FROM cleaned_public_data", conn)

# Filter the dataset
public_data['is_relevant'] = public_data['cleaned_text'].apply(lambda x: is_relevant(x, chatgpt_patterns, education_patterns, exclude_patterns, negative_context_patterns))
filtered_public_data = public_data[public_data['is_relevant']].drop(columns=['is_relevant'])

# Save the filtered data to a new table in the database
filtered_public_data.to_sql('filtered_public_data', conn, if_exists='replace', index=False)

conn.close()

print(f"Total documents before filtering: {len(public_data)}")
print(f"Total documents after filtering: {len(filtered_public_data)}")
print("Filtered public data saved to the SQLite database in a new table.")
