from tkinter import Toplevel, Label, Entry, Button, messagebox

# カスタムダイアログウィンドウを作成する関数
def ask_year_and_number():
    def submit():
        year_value = year_entry.get().strip()
        number_value = number_entry.get().strip()
        if year_value and number_value:
            result[0] = (year_value, number_value)
            dialog.destroy()
        else:
            messagebox.showwarning("入力エラー", "年度と問題番号を入力してください。")

    dialog = Toplevel()
    dialog.title("年度と問題番号の入力")
    dialog.transient()  # 親ウィンドウに対してモーダルな挙動に
    dialog.grab_set()   # 他のウィンドウの操作を一時的に無効にする

    Label(dialog, text="年度:").grid(row=0, column=0, padx=5, pady=5)
    year_entry = Entry(dialog)
    year_entry.grid(row=0, column=1, padx=5, pady=5)

    Label(dialog, text="問題番号:").grid(row=1, column=0, padx=5, pady=5)
    number_entry = Entry(dialog)
    number_entry.grid(row=1, column=1, padx=5, pady=5)

    Button(dialog, text="OK", command=submit).grid(row=2, column=1, padx=5, pady=5)

    result = [None]
    dialog.wait_window()  # ユーザーがダイアログを閉じるまで待つ
    return result[0]
