import tkinter as tk
from functools import partial
import logging

# クリップボードにテキストをコピーする関数
def copy_to_clipboard(app, option_idx):
    if hasattr(app, 'current_question') and app.current_question:
        if option_idx < len(app.current_question['選択肢']):
            text = app.current_question['選択肢'][option_idx]
            app.root.clipboard_clear()  # クリップボードをクリア
            app.root.clipboard_append(text)  # クリップボードにテキストをコピー
            app.root.update()  # クリップボードの更新
            app.update_status_label(f"選択肢 {option_idx + 1} をクリップボードにコピーしました")

# UIのセットアップ（answer_buttonsの部分）
def setup_answer_buttons(app, default_font):
    logging.debug("Setting up answer buttons")

    # wraplengthの定義（ここで一括管理）
    wraplength_value = 600

    app.answer_buttons = []
    button_frame = tk.Frame(app.frame)
    button_frame.pack(fill=tk.BOTH, expand=True)

    for i in range(4):
        # 選択肢ボタン（wraplengthを変数で管理）
        button = tk.Button(button_frame, text=f"選択肢 {i + 1}", command=partial(app.check_answer, i),
                           font=default_font, wraplength=wraplength_value)  # wraplengthを変数から設定
        button.grid(row=i, column=0, sticky="w", padx=5, pady=2)
        app.answer_buttons.append(button)

        # 読み上げボタン（wraplengthを変数で管理）
        read_button = tk.Button(button_frame, text=f"選択肢 {i + 1} を読み上げ", command=partial(app.read_aloud_option, i),
                                wraplength=wraplength_value)  # wraplengthを変数から設定
        read_button.grid(row=i, column=1, sticky="w", padx=5, pady=2)

        # クリップボードにコピーするボタン（wraplengthを変数で管理）
        copy_button = tk.Button(button_frame, text=f"選択肢 {i + 1} をコピー", command=partial(copy_to_clipboard, app, i),
                                wraplength=wraplength_value)  # wraplengthを変数から設定
        copy_button.grid(row=i, column=2, sticky="w", padx=5, pady=2)

    # 次の問題ボタン
    app.next_button = tk.Button(app.frame, text="次の問題", state=tk.DISABLED, command=app.next_question)
    app.next_button.pack(anchor="w", pady=5)

    logging.debug("Answer buttons setup complete")
