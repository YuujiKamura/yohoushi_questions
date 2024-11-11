import json

def save_question(file_path, question_data):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(question_data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving question to {file_path}: {e}")
