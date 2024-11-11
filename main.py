import json
import tkinter as tk
from tkinter import simpledialog, font

from utils import open_json_editor
from utils.get_sorted_question_files import get_sorted_question_files
from utils.ui_setup import setup_question_selection_ui, setup_buttons, setup_labels, setup_answer_buttons
from utils.reading_control import stop_reading, read_aloud_option, read_aloud_reason
from utils.create_new_question import create_new_question
from question_logic import display_question, select_question, check_answer, next_question, refresh_question_list  # 問題関連のロジックをインポート
import pyttsx3
import threading
import os

# Main GUI application class
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("予報士問題 学習支援アプリ")

        # デフォルトフォントを設定
        default_font = font.Font(family="Helvetica", size=12)

        # 問題ファイルの取得
        self.question_files = get_sorted_question_files()
        self.current_question = None
        self.current_index = -1

        # 読み上げ用のロックと停止イベントを初期化
        self.reading_lock = threading.Lock()
        self.stop_event = threading.Event()

        # テキスト読み上げエンジンの初期化
        self.engine = pyttsx3.init()

        # メインフレームの作成
        self.frame = tk.Frame(self.root, padx=10, pady=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # UIのセットアップ
        setup_question_selection_ui(self, None)
        setup_buttons(self, None)
        setup_labels(self, None)
        setup_answer_buttons(self, None)

        # 状態表示用ラベル
        self.engine_status_label = tk.Label(self.frame, text="読み上げ状態: 停止中")
        self.engine_status_label.pack(anchor="w")

        # 解説用のテキストウィジェット
        self.explanation_text = tk.Text(self.frame, height=10, state=tk.DISABLED, wrap=tk.WORD)
        self.explanation_text.pack(fill=tk.BOTH, expand=True)

        # 初期表示の問題
        display_question(self)

    def create_new_question(self):
        """
        新しい問題を作成するメソッド。外部の utils/create_new_question.py を呼び出す。
        """
        create_new_question(self)

    def select_question(self):
        """
        リストから選択した問題を表示する
        """
        select_question(self)

    def edit_question(self):
        """
        既存の問題を編集するメソッド。
        """
        selection = self.question_listbox.curselection()
        if selection:
            file_path = os.path.join('questions', self.question_files[selection[0]])

            # ファイルからJSONを読み込み、年度と番号を取得
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # 問題年度と問題番号を取得
                year_value = data.get('問題年度', '')
                number_value = data.get('問題番号', '')

                # open_json_editor関数に年度と番号を渡す
                open_json_editor(file_path, year_value, number_value, self.refresh_question_list)

    def rename_question_file(self, event):
        """
        問題ファイルの名前を変更するメソッド。
        """
        selection = self.question_listbox.curselection()
        if selection:
            old_file_path = os.path.join('questions', self.question_files[selection[0]])
            new_name = simpledialog.askstring("ファイル名変更", "新しいファイル名を入力してください：",
                                              initialvalue=self.question_files[selection[0]])
            if new_name and new_name != self.question_files[selection[0]]:
                new_file_path = os.path.join('questions', new_name)
                os.rename(old_file_path, new_file_path)
                self.refresh_question_list()

    def read_aloud_option(self, option_idx):
        """
        指定された選択肢を読み上げるメソッド。
        :param option_idx: 読み上げたい選択肢のインデックス
        """
        if hasattr(self, 'current_question') and self.current_question:
            read_aloud_option(self, option_idx)

    def stop_reading(self):
        """
        読み上げを停止するメソッド。
        """
        stop_reading(self)

    def check_answer(self, user_answer_idx):
        """
        ユーザーが選択した解答をチェックする
        """
        check_answer(self, user_answer_idx)

    def next_question(self):
        """
        次の問題に移動
        """
        next_question(self)

    def refresh_question_list(self):
        """
        リストボックスをリフレッシュして、問題ファイルを更新する
        """
        refresh_question_list(self)

    def update_status_label(self, status_text):
        """
        読み上げ状態を表示するラベルを更新するメソッド。
        :param status_text: 表示するステータスのテキスト
        """
        self.engine_status_label.config(text=status_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
