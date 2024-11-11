import json
import os

# 問題ファイルを読み込む関数
def load_question(file_path):
    """
    指定されたJSONファイルから問題を読み込む関数。
    :param file_path: 読み込む問題ファイルのパス
    :return: JSONデータを辞書形式で返す。ファイルがない場合は空の辞書を返す。
    """
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# JSONファイルをソートしてリストとして返す関数
def get_sorted_question_files():
    """
    questionsディレクトリ内のすべてのJSONファイルをソートして返す関数。
    :return: ソートされたファイル名のリスト。
    """
    question_dir = os.path.join(os.path.dirname(__file__), '../questions')
    if os.path.exists(question_dir):
        return sorted([f for f in os.listdir(question_dir) if f.endswith('.json')])
    return []

# ファイルからカテゴリを取得する関数
def get_category_from_file(file_path):
    """
    指定されたJSONファイルからカテゴリを抽出する関数。
    :param file_path: カテゴリ情報が含まれている問題ファイルのパス
    :return: カテゴリ名（見つからない場合は '不明' を返す）
    """
    full_path = os.path.join(os.path.dirname(__file__), '../questions', file_path)
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # JSON内のカテゴリ情報が "category" というキーで保存されていると仮定
            return data.get('category', '不明')
    return '不明'

# 問題ファイルを保存する関数（追加例）
def save_question(file_path, data):
    """
    指定されたデータを問題ファイルに保存する関数。
    :param file_path: 保存するファイルのパス
    :param data: 保存するデータ（辞書形式）
    """
    full_path = os.path.join(os.path.dirname(__file__), '../questions', file_path)
    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

