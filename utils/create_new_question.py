import json
import os
from question_logic import display_question

def create_new_question(app):
    """
    新しい問題を作成し、ファイルに保存する関数。
    :param app: QuizApp インスタンス
    """
    new_question_data = {
        "問題": "新しい問題をここに作成します",
        "問題年度": "未設定",
        "通算": "未設定",
        "学科種別": "未設定",
        "問題番号": "未設定",
        "問題タイプ": "正しいものを選ぶ",
        "問題肢": [
            "(a) 問題肢1の内容をここに記述します。",
            "(b) 問題肢2の内容をここに記述します。",
            "(c) 問題肢3の内容をここに記述します。",
            "(d) 問題肢4の内容をここに記述します。"
        ],
        "選択肢": [
            "① 選択肢1",
            "② 選択肢2",
            "③ 選択肢3",
            "④ 選択肢4"
        ],
        "正解番号": 1,
        "解説": [
            "選択肢1に関する解説をここに記述します。",
            "選択肢2に関する解説をここに記述します。",
            "選択肢3に関する解説をここに記述します。",
            "選択肢4に関する解説をここに記述します。"
        ],
        "カテゴリ": "未設定",
        "キーワード": [
            "キーワード1", "キーワード2", "キーワード3"
        ],
        "理解度": 0.0,
        "画像リンク": "None"
    }

    # ファイル名を指定して保存
    file_name = f"new_question_{len(app.question_files) + 1}.json"
    file_path = os.path.join('questions', file_name)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(new_question_data, f, ensure_ascii=False, indent=4)

    # 問題リストの更新と表示
    app.refresh_question_list()  # 問題リストを更新
    app.current_question = new_question_data  # 新しい問題をセット
    display_question(app)  # 新しい問題を表示
