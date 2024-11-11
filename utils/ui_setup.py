import tkinter as tk
from tkinter import font
import logging
from utils.get_sorted_question_files import get_category_from_file
from utils.ui_answer_buttons import setup_answer_buttons
from utils.explanation_buttons import setup_or_refresh_explanation_buttons

def setup_ui(app):
    logging.debug("Starting UI setup")

    # 画面の幅と高さを取得して、半分の幅でウィンドウサイズを設定
    screen_width = app.root.winfo_screenwidth()  # 画面の幅を取得
    screen_height = app.root.winfo_screenheight()  # 画面の高さを取得
    app_width = screen_width // 2  # 幅を半分に
    app_height = screen_height  # 高さはそのまま全体に設定

    # ウィンドウのサイズを設定（画面の半分の幅、全体の高さ）
    app.root.geometry(f'{app_width}x{app_height}')
    app.root.resizable(False, False)  # ウィンドウサイズを変更不可にする

    # フォントの設定（ここで全体のフォントサイズを変更可能）
    default_font = font.Font(family="Helvetica", size=14)

    app.frame = tk.Frame(app.root, padx=10, pady=10)
    app.frame.pack(fill=tk.BOTH, expand=True)

    # 各UI要素にフォントを設定
    setup_question_selection_ui(app, default_font)  # default_fontを渡す
    setup_buttons(app, default_font)
    setup_labels(app, default_font)
    setup_answer_buttons(app, default_font)

    # 解説用のテキストウィジェットを初期化（折り返し設定を追加）
    app.explanation_text = tk.Text(app.frame, height=10, state=tk.DISABLED, wrap=tk.WORD, font=default_font)
    app.explanation_text.pack(fill=tk.BOTH, expand=True)

    # 解説ボタンをセットアップまたはリフレッシュ
    setup_or_refresh_explanation_buttons(app, [])

    logging.debug("UI setup complete")


def setup_question_selection_ui(app, default_font):
    logging.debug("Setting up question selection UI")

    # ラベルを表示（問題選択ラベル、折り返しは不要）
    label = tk.Label(app.frame, text="問題選択", font=default_font)
    label.pack(anchor="w")

    # リストボックスを作成（ルートのバージョンを統合）
    app.question_listbox = tk.Listbox(app.frame, font=default_font, selectmode=tk.SINGLE)
    app.question_listbox.pack(fill=tk.BOTH, expand=True)

    # ダブルクリックで問題を選択するイベントをバインド
    app.question_listbox.bind("<Double-Button-1>", lambda event: app.select_question())

    # ファイル名とカテゴリをリストボックスに表示
    for question_file in app.question_files:
        category = get_category_from_file(question_file)
        app.question_listbox.insert(tk.END, f"{question_file} - {category}")

    logging.debug("Question selection UI setup complete with %d questions.", len(app.question_files))


def setup_buttons(app, default_font):
    logging.debug("Setting up buttons")

    # 新しい問題作成ボタン
    app.new_question_button = tk.Button(app.frame, text="新しい問題を作成", command=app.create_new_question, font=default_font)
    app.new_question_button.pack(anchor="w")

    # 既存の問題編集ボタン
    app.edit_question_button = tk.Button(app.frame, text="既存の問題を編集", command=app.edit_question, font=default_font)
    app.edit_question_button.pack(anchor="w")

    # 次の問題に進むボタン（ルートから統合）
    app.next_button = tk.Button(app.frame, text="次の問題", command=app.next_question, font=default_font)
    app.next_button.pack(side=tk.BOTTOM)

    logging.debug("Buttons setup complete")


def setup_labels(app, default_font):
    logging.debug("Setting up labels")

    # 問題文ラベル、折り返し設定を追加
    app.question_label = tk.Label(app.frame, text="問題: 未選択", font=default_font, wraplength=1800)  # 1800ピクセルで折り返し
    app.question_label.pack(anchor="w")

    # 問題情報ラベル、折り返し設定を追加
    app.question_info_label = tk.Label(app.frame, text="問題情報: 未選択", font=default_font, wraplength=1800)
    app.question_info_label.pack(anchor="w")

    # 結果ラベル（結果が長い場合も想定して折り返し設定）
    app.result_label = tk.Label(app.frame, text="結果: 未選択", font=default_font, wraplength=1800)
    app.result_label.pack(anchor="w")

    logging.debug("Labels setup complete")

