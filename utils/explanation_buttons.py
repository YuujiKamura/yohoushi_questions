import tkinter as tk  # tkinterをインポート
from functools import partial
import logging  # loggingをインポート


def setup_or_refresh_explanation_buttons(app, explanations):
    """
    Set up or refresh explanation buttons and update the explanation text widget.
    :param app: The app instance where buttons and text widget exist.
    :param explanations: List of explanations to display.
    """
    # 古いフレームが存在すれば削除
    if hasattr(app, 'button_frame') and app.button_frame:
        app.button_frame.destroy()

    # 新しいフレームを作成
    app.button_frame = tk.Frame(app.frame)
    app.button_frame.pack(fill=tk.BOTH, expand=True, pady=5)

    # ボタンリストを初期化
    app.explanation_buttons = []

    if explanations:
        for i, explanation in enumerate(explanations):
            def on_button_click(explanation_index):
                # 読み上げ機能の呼び出し
                app.read_aloud_information(explanation_index)
                # テキストウィジェットに解説を表示
                show_explanation_in_text_widget(app.explanation_text, explanations[explanation_index])

            # 解説読み上げボタンの作成
            read_aloud_button = tk.Button(app.button_frame, text=f"解説{i + 1}を読み上げ",
                                          command=partial(on_button_click, i))
            read_aloud_button.pack(anchor="w", side=tk.LEFT, padx=5)
            app.explanation_buttons.append(read_aloud_button)
    else:
        # 解説がない場合にプレースホルダーボタンを表示
        placeholder_button = tk.Button(app.button_frame, text="解説がありません")
        placeholder_button.pack(anchor="w", side=tk.LEFT, padx=5)
        app.explanation_buttons.append(placeholder_button)

    # テキストウィジェットも初期化
    show_explanation_in_text_widget(app.explanation_text, "解説が選択されていません")



# テキストウィジェットに解説を表示する関数
def show_explanation_in_text_widget(text_widget, explanation):
    """
    Display the explanation text in the provided text widget.
    :param text_widget: The text widget to display the explanation.
    :param explanation: The explanation text to display.
    """
    text_widget.config(state=tk.NORMAL)  # テキストウィジェットを編集可能に
    text_widget.delete(1.0, tk.END)  # テキストウィジェット内をクリア
    text_widget.insert(tk.END, explanation)  # 新しい解説を挿入
    text_widget.config(state=tk.DISABLED)  # 再び編集不可に設定
