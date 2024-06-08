import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Enhanced ToDo App')
        self.tasks = {}

        # タスク入力フィールド
        self.task_entry = tk.Entry(self.root, width=50)
        self.task_entry.pack(pady=10)
        self.task_entry.bind('<Return>', self.add_task)

        # タスク追加ボタン
        add_task_button = tk.Button(self.root, text='Add Task', command=self.add_task)
        add_task_button.pack(pady=10)

        # タスクリスト表示エリア
        self.tasks_listbox = tk.Listbox(self.root, width=50, height=10)
        self.tasks_listbox.pack(pady=20)

        # フィルター選択コンボボックス
        self.status_filter = ttk.Combobox(self.root, values=["All", "Done", "Todo"])
        self.status_filter.set("All")
        self.status_filter.pack(pady=10)
        self.status_filter.bind("<<ComboboxSelected>>", self.update_listbox)

        # タスク完了トグルボタン
        toggle_button = tk.Button(self.root, text='Toggle Done', command=self.toggle_task_done)
        toggle_button.pack(pady=10)

        # タスク削除ボタン
        delete_task_button = tk.Button(self.root, text='Delete Task', command=self.delete_task)
        delete_task_button.pack(pady=10)

        # Bind keys for Vim-style navigation
        self.tasks_listbox.bind('j', self.move_down)
        self.tasks_listbox.bind('k', self.move_up)

        # ショートカットキーの説明を表示するボタン
        shortcut_button = tk.Button(self.root, text='Show Shortcuts<Ctrl+H>', command=self.show_shortcuts)
        shortcut_button.pack(pady=10)

        # ショートカットキーのバインディング
        self.root.bind('<Control-a>', lambda event: self.add_task())
        self.root.bind('<Control-d>', lambda event: self.delete_task())
        self.root.bind('<Control-t>', lambda event: self.toggle_task_done())
        self.root.bind('<Control-f>', lambda event: self.cycle_filter())
        self.root.bind('<Control-e>', lambda event: self.task_entry.focus())  # 入力フィールドにフォーカスを当てる
        self.root.bind('<Control-h>', lambda event: self.show_shortcuts())
        self.root.bind('<Control-l>', lambda event: self.focus_first_task())

    def show_shortcuts(self):
        # ショートカットキーの説明を表示
        shortcuts = (
            "Ctrl+A: 新しいタスクを追加\n"
            "Ctrl+D: 選択したタスクを削除\n"
            "Ctrl+F: フィルターを切り替え\n"
            "Ctrl+E: 入力フィールドにフォーカス\n"
            "Ctrl+L: リストの最初のタスクにフォーカス"
        )
        messagebox.showinfo("Keyboard Shortcuts", shortcuts)
        self.root.focus_force()  # フォーカスを強制的に戻す

    def add_task(self, event=None):
        # タスクを追加
        task = self.task_entry.get()
        if task:
            self.tasks[task] = False
            self.update_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("警告", "空では登録できません。")
            self.root.focus_force()  # フォーカスを強制的に戻す

    def update_listbox(self, event=None):
        # リストボックスを更新
        filter_option = self.status_filter.get()
        self.tasks_listbox.delete(0, tk.END)
        for task, done in self.tasks.items():
            if (filter_option == "All" or
                (filter_option == "Done" and done) or
                (filter_option == "Todo" and not done)):
                display_text = f"[{'DONE' if done else 'TODO'}] {task}"
                self.tasks_listbox.insert(tk.END, display_text)

    def toggle_task_done(self):
        # タスクの完了状態をトル
        try:
            index = self.tasks_listbox.curselection()[0]  # 現在選択されているタスクのインデックスを取得
            task = list(self.tasks.keys())[index]  # タスクを特定
            self.tasks[task] = not self.tasks[task]  # タスクの完了状態を反転
            self.update_listbox()  # リストボックスを更新

            # リスト更新後にタスクに再びフォーカスを設定
            self.tasks_listbox.selection_set(index)  # タスクを選択状態にする
            self.tasks_listbox.see(index)  # 選択したタスクが表示されるようにスクロールする
            self.tasks_listbox.activate(index)  # 選択したタスクをアクティブにする
        except IndexError:
            messagebox.showwarning("警告", "トグルするタスクを選択してください。")
            self.root.focus_force()  # フォーカスを強制的に戻す

    def delete_task(self):
        # 選択されたタスクのインデックスを取得
        try:
            index = self.tasks_listbox.curselection()[0]
            task = list(self.tasks.keys())[index]  # 辞書からタスクを特定
            del self.tasks[task]  # 辞書からタスクを削除
            self.update_listbox()  # リストボックスを更新

            # タスクの削除後、フォーカスを調整
            if self.tasks_listbox.size() > 0:  # まだタスクが残っているか確認
                new_index = index if index < self.tasks_listbox.size() else index - 1
                self.tasks_listbox.select_set(new_index)  # 新しいインデックスを選択
                self.tasks_listbox.see(new_index)  # 新しいインデックスが表示されるようにスクロール
                self.tasks_listbox.activate(new_index)  # 新しいインデックスをアクティブにする
        except IndexError:
            messagebox.showwarning("警告", "削除するタスクを選択してください。")
            self.root.focus_force()  # フォーカスを強制的に戻す

    def cycle_filter(self):        # フィルターオプションを循環させる
        current_index = ["All", "Done", "Todo"].index(self.status_filter.get()) + 1
        new_filter = ["All", "Done", "Todo"][current_index % 3]
        self.status_filter.set(new_filter)
        self.update_listbox()

    def move_down(self, event):
        current_index = self.tasks_listbox.curselection()
        if current_index:
            next_index = current_index[0] + 1
            if next_index < self.tasks_listbox.size():
                self.tasks_listbox.select_clear(current_index)
                self.tasks_listbox.select_set(next_index)
                self.tasks_listbox.see(next_index)

    def move_up(self, event):
        current_index = self.tasks_listbox.curselection()
        if current_index:
            next_index = current_index[0] - 1
            if next_index >= 0:
                self.tasks_listbox.select_clear(current_index)
                self.tasks_listbox.select_set(next_index)
                self.tasks_listbox.see(next_index)

    def focus_first_task(self, event=None):
        if self.tasks_listbox.size() > 0:
            self.tasks_listbox.focus_set()  # Focus the Listbox
            self.tasks_listbox.select_set(0)  # Select the first item
            self.tasks_listbox.see(0)  # Ensure the first item is visible

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
