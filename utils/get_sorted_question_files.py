import logging
import os
import json
import re
import tkinter as tk

# 自然順でファイル名をソートする関数
def get_sorted_question_files():
    if not os.path.exists('questions'):
        logging.error("'questions' ディレクトリが見つかりません。")
        return []

    files = [f for f in os.listdir('questions') if f.endswith('.json')]

    if not files:
        logging.warning("'questions' ディレクトリ内にJSONファイルが存在しません。")
        return []

    def natural_sort_key(file_name):
        return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', file_name)]

    return sorted(files, key=natural_sort_key)

# カテゴリをファイルから読み込む関数
def get_category_from_file(file_name):
    file_path = os.path.join('questions', file_name)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                category = data.get('カテゴリ', 'カテゴリ不明')
                if category != 'カテゴリ不明':
                    logging.debug(f"カテゴリ取得成功: {file_name} => カテゴリ: {category}")
                else:
                    logging.warning(f"カテゴリ不明: {file_name}")
                return category
            except json.JSONDecodeError:
                logging.error(f"ファイル {file_name} の読み込み中にJSONエラーが発生しました。")
                return 'カテゴリ不明'
    else:
        logging.error(f"ファイルが存在しません: {file_name}")
        return 'カテゴリ不明'

# リストボックスにファイル名とカテゴリを表示する関数
def setup_question_selection_ui(app):
    logging.debug("Setting up question selection UI")

    label = tk.Label(app.frame, text="問題選択")
    label.pack(anchor="w")

    app.question_listbox = tk.Listbox(app.frame)
    app.question_listbox.pack(fill=tk.BOTH, expand=True)
    app.question_listbox.bind("<Double-Button-1>", lambda event: app.select_question())

    # 自然順にソートされたファイル名を取得
    sorted_files = get_sorted_question_files()

    if not sorted_files:
        logging.error("問題ファイルが見つかりません。")
        return

    for question_file in sorted_files:
        category = get_category_from_file(question_file)
        logging.debug(f"カテゴリ表示: ファイル名: {question_file}, カテゴリ: {category}")
        app.question_listbox.insert(tk.END, f"{question_file} (カテゴリ: {category})")

    logging.debug("Question selection UI setup complete with %d questions.", len(sorted_files))


# テスト用にシンプルなTkinterアプリケーションを定義
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("問題選択アプリ")

        self.frame = tk.Frame(self.root, padx=10, pady=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        setup_question_selection_ui(self)

    def select_question(self):
        selection = self.question_listbox.curselection()
        if selection:
            selected_file = self.question_listbox.get(selection)
            logging.info(f"選択された問題: {selected_file}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
