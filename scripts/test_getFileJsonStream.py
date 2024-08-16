import json
from fileStreams import getFileJsonStream

def test_getFileJsonStream(file_path):
    json_stream = getFileJsonStream(file_path)
    if json_stream is not None:
        for line_number, row in json_stream:
            print(f"Line {line_number}: {row}")
            break  # Read only the first line for testing
    else:
        print(f"Could not open JSON stream for file: {file_path}")

# Test with your files
test_getFileJsonStream('/Users/vesper/Desktop/LSE/Capstone Project/dissertation/data/r_ChatGPT_posts.jsonl')
test_getFileJsonStream('/Users/vesper/Desktop/LSE/Capstone Project/dissertation/data/r_ChatGPT_comments.jsonl')
