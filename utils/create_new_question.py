# utils/create_new_question.py
import json
import os

def create_new_question(app):
    """
    新しい問題を作成し、ファイルに保存する関数。
    :param app: QuizApp インスタンス
    """
    new_question_data = {
        '問題': '新しい問題をここに作成します',
        '選択肢': ['選択肢1', '選択肢2', '選択肢3', '選択肢4'],
        '正解番号': 1,
        '解説': ['解説1', '解説2', '解説3', '解説4']
    }

    # ファイル名を指定して保存
    file_name = f"new_question_{len(app.question_files) + 1}.json"
    file_path = os.path.join('questions', file_name)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(new_question_data, f, ensure_ascii=False, indent=4)

    app.refresh_question_list()  # 問題リストを更新
    app.current_question = new_question_data  # 新しい問題をセット
    app.display_question()  # 新しい問題を表示
