import os

def get_question_files(directory='questions'):
    try:
        return [f for f in os.listdir(directory) if f.endswith('.json')]
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.")
        return []
