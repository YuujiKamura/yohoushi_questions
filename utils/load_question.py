import json

def load_question(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            question_data = json.load(file)
            return question_data
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file {file_path}: {e}")
        return None
