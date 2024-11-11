# question_logic.py
import os
from utils.data_handling import load_question, get_sorted_question_files, get_category_from_file
import tkinter as tk  # 追加する部分

def display_question(app):
    """
    現在のインデックスに対応する問題を表示する
    """
    if app.current_index < len(app.question_files):
        file_path = os.path.join('questions', app.question_files[app.current_index])
        app.current_question = load_question(file_path)

        # 問題文の表示
        question_text = app.current_question['問題']
        # 問題肢が存在する場合のみ改行で連結
        if '問題肢' in app.current_question and app.current_question['問題肢']:
            options_text = "\n".join(app.current_question['問題肢'])
            app.question_label.config(text=f"問題: {question_text}\n\n{options_text}")
        else:
            app.question_label.config(text=f"問題: {question_text}")

        # 問題情報の表示
        app.question_info_label.config(
            text=f"問題年度: {app.current_question['問題年度']} / 通算: {app.current_question['通算']} / 問題番号: {app.current_question['問題番号']} / 種別: {app.current_question['学科種別']}"
        )

        # 各選択肢の表示
        for idx, option in enumerate(app.current_question['選択肢']):
            if idx < len(app.answer_buttons):  # ボタンの数を選択肢に合わせる
                app.answer_buttons[idx].config(text=option, state=tk.NORMAL)
            else:
                # 必要なボタンが足りない場合、新しいボタンを生成するロジックが必要です
                pass

        # 結果表示をクリア
        app.result_label.config(text="")

        # 解説、カテゴリ、キーワードなどの設定
        app.explanation_text.delete('1.0', tk.END)  # テキストをクリア
        app.explanation_text.insert(tk.END, f"解説: {' / '.join(app.current_question['解説'])}")

        # カテゴリとキーワードはLabelウィジェットを使っている場合
        app.category_label.config(text=f"カテゴリ: {app.current_question['カテゴリ']}")
        app.keyword_label.config(text=f"キーワード: {', '.join(app.current_question['キーワード'])}")


def select_question(app):
    """
    リストから選択した問題を表示する
    """
    selection = app.question_listbox.curselection()
    if selection:
        app.current_index = selection[0]
        display_question(app)

def check_answer(app, user_answer_idx):
    """
    ユーザーが選択した解答をチェックする
    """
    correct_answer_idx = app.current_question['正解番号'] - 1
    if user_answer_idx == correct_answer_idx:
        app.result_label.config(text=f"正解！ あなたの選択: {user_answer_idx + 1} / 正解: {correct_answer_idx + 1}")
        app.read_aloud("正解です！")
    else:
        app.result_label.config(text=f"不正解。あなたの選択: {user_answer_idx + 1} / 正解: {correct_answer_idx + 1}")
        app.read_aloud("不正解です。")

def next_question(app):
    """
    次の問題に移動
    """
    app.current_index += 1
    if app.current_index < len(app.question_files):
        display_question(app)
    else:
        app.result_label.config(text="すべての問題を完了しました。")

def refresh_question_list(app):
    """
    リストボックスをリフレッシュして、問題ファイルを更新する
    """
    app.question_files = get_sorted_question_files()
    app.question_listbox.delete(0, tk.END)

    # 各ファイルのカテゴリを取得してリストに表示
    for question_file in app.question_files:
        category = get_category_from_file(question_file)
        app.question_listbox.insert(tk.END, f"{question_file} - カテゴリ: {category}")
