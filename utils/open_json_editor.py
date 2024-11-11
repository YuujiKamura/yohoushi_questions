import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime
def open_json_editor(file_path, year_value, number_value, on_save_callback=None):
    def save_json():
        try:
            # JSONのデータを取得
            updated_data = json.loads(text_area.get("1.0", tk.END))

            # 入力された年度と番号を取得
            year_input = year_entry.get().strip()
            number_input = number_entry.get().strip()

            # 年度を設定
            updated_data['問題年度'] = year_input if year_input else year_value
            # 問題番号を設定
            updated_data['問題番号'] = number_input if number_input else number_value

            # 新しいファイル名を取得
            new_file_name = file_name_entry.get().strip()
            if new_file_name:
                new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
            else:
                new_file_path = file_path

            # 既存ファイルがあれば削除して、新しいファイル名で保存
            if new_file_path != file_path:
                os.remove(file_path)

            # JSONファイルに保存
            with open(new_file_path, 'w', encoding='utf-8') as f:
                json.dump(updated_data, f, ensure_ascii=False, indent=4)

            # コールバックがあれば実行
            if on_save_callback:
                on_save_callback()

            editor_window.destroy()
        except json.JSONDecodeError as e:
            messagebox.showerror("JSONエラー", f"JSONの形式に誤りがあります:\n{str(e)}")

    # エディタウィンドウの作成
    editor_window = tk.Toplevel()
    editor_window.title(f"JSONエディタ - {file_path}")

    # ファイル名の入力フィールドを追加
    file_name_label = tk.Label(editor_window, text="ファイル名:")
    file_name_label.pack(anchor="w")
    file_name_entry = tk.Entry(editor_window)
    file_name_entry.insert(0, os.path.basename(file_path))  # 現在のファイル名を表示
    file_name_entry.pack(anchor="w", fill=tk.X)

    # 年度と番号の入力フィールドを追加
    year_label = tk.Label(editor_window, text="問題年度:")
    year_label.pack(anchor="w")
    year_entry = tk.Entry(editor_window)
    year_entry.insert(0, year_value)
    year_entry.pack(anchor="w", fill=tk.X)

    number_label = tk.Label(editor_window, text="問題番号:")
    number_label.pack(anchor="w")
    number_entry = tk.Entry(editor_window)
    number_entry.insert(0, number_value)
    number_entry.pack(anchor="w", fill=tk.X)

    # JSONデータの読み込み
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        # ファイルが存在しない場合、空のJSONデータを初期化
        data = {
            "問題": "",
            "問題タイプ": "",
            "選択肢": [],
            "正解番号": 0,
            "理由": "",
            "問題年度": "",
            "問題番号": "",
            "カテゴリ": "",
            "キーワード": [],
            "理解度": 0.0,
            "付帯情報": "",
            "画像リンク": ""
        }

    # テキストエリア
    text_area = tk.Text(editor_window, wrap=tk.WORD, width=80, height=30)
    text_area.insert(tk.END, json.dumps(data, ensure_ascii=False, indent=4))
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # 保存ボタン
    save_button = tk.Button(editor_window, text="保存", command=save_json)
    save_button.pack(side=tk.LEFT, padx=10, pady=10)

    # 閉じるボタン
    close_button = tk.Button(editor_window, text="閉じる", command=editor_window.destroy)
    close_button.pack(side=tk.RIGHT, padx=10, pady=10)
