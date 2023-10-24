import pandas as pd
import random
import tkinter as tk
from tkinter import messagebox

class VocabularyGame:
    def __init__(self, root):
        self.root = root
        self.root.title("單字練習程式")
        self.word_csv = pd.read_csv('TSMC_words.csv', header=None)
        self.wordlist = self.word_csv.values.tolist()
        random.shuffle(self.wordlist)  # 打亂題目的順序
        self.game_mode = tk.StringVar()
        self.num_questions = tk.StringVar()

        # 顯示遊戲模式的標籤和選項
        self.mode_label = tk.Label(root, text="請選擇遊戲模式：")
        self.mode_label.pack()
        self.radio_button1 = tk.Radiobutton(root, text="英文翻中文", variable=self.game_mode, value="english_to_chinese")
        self.radio_button1.pack()
        self.radio_button2 = tk.Radiobutton(root, text="中文翻英文", variable=self.game_mode, value="chinese_to_english")
        self.radio_button2.pack()

        # 顯示選擇題數的標籤和輸入框
        self.num_questions_label = tk.Label(root, text="請輸入題數：")
        self.num_questions_label.pack()
        self.num_questions_entry = tk.Entry(root, textvariable=self.num_questions)
        self.num_questions_entry.pack()

        # 顯示開始按鈕
        self.start_button = tk.Button(root, text="開始遊戲", command=self.start_game)
        self.start_button.pack()

        # 初始化變數
        self.current_question = 0
        self.correct = 0
        self.wrong = 0
        self.wrong_list = []

    def start_game(self):
        # 檢查是否選擇了遊戲模式和輸入了題數
        if not self.game_mode.get() or not self.num_questions.get().isdigit():
            messagebox.showwarning("錯誤", "請選擇遊戲模式並輸入有效的題數。")
            return

        # 取得遊戲模式和題數
        mode = self.game_mode.get()
        num_questions = int(self.num_questions.get())

        # 顯示題目的標籤
        if mode == "english_to_chinese":
            self.question_label = tk.Label(self.root, text=self.wordlist[self.current_question][0])
        else:
            self.question_label = tk.Label(self.root, text=self.wordlist[self.current_question][1])
        self.question_label.pack()

        # 顯示輸入答案的標籤和輸入框
        self.entry_label = tk.Label(self.root, text="請輸入答案：")
        self.entry_label.pack()
        self.entry_box = tk.Entry(self.root)
        self.entry_box.pack()

        # 顯示下一題按鈕
        self.next_button = tk.Button(self.root, text="下一題", command=self.next_question)
        self.next_button.pack()

        # 設定遊戲題數
        self.num_questions_left = num_questions

    def next_question(self):
        # 獲取使用者輸入的答案
        user_answer = self.entry_box.get()

        # 檢查答案是否正確
        if self.game_mode.get() == "english_to_chinese":
            if user_answer == self.wordlist[self.current_question][1]:
                self.correct += 1
            else:
                self.wrong += 1
                self.wrong_list.append(self.current_question)
        else:
            if user_answer == self.wordlist[self.current_question][0]:
                self.correct += 1
            else:
                self.wrong += 1
                self.wrong_list.append(self.current_question)

        # 移至下一題或顯示結果
        self.current_question += 1
        self.num_questions_left -= 1

        if self.num_questions_left > 0 and self.current_question < len(self.wordlist):
            if self.game_mode.get() == "english_to_chinese":
                self.question_label.config(text=self.wordlist[self.current_question][0])
            else:
                self.question_label.config(text=self.wordlist[self.current_question][1])
            self.entry_box.delete(0, tk.END)  # 清空輸入框
        else:
            self.show_results()

    def show_results(self):
        # 顯示結果
        result_message = f"答對數量: {self.correct}\n答錯數量: {self.wrong}\n\n"
        result_message += "答錯的題目與答案：\n"
        for i in self.wrong_list:
            if self.game_mode.get() == "english_to_chinese":
                result_message += f"{self.wordlist[i][0]} -> {self.wordlist[i][1]}\n"
            else:
                result_message += f"{self.wordlist[i][1]} -> {self.wordlist[i][0]}\n"

        import os
        from datetime import datetime
        now = str(datetime.now().time())  #summary name
        now = ('{:.8s}'.format(now))
        os.chdir('summary')
        with open(f'{now}.txt', 'w') as f:
            f.write(result_message)



        messagebox.showinfo("遊戲結果", result_message)

        # 重設遊戲變數
        self.current_question = 0
        self.correct = 0
        self.wrong = 0
        self.wrong_list = []
        self.question_label.config(text="")  # 清空題目標籤
        self.entry_box.delete(0, tk.END)  # 清空輸入框
        self.num_questions_left = 0
        self.root.quit()  # 退出遊戲

# 啟動視窗
if __name__ == "__main__":
    root = tk.Tk()
    game = VocabularyGame(root)
    root.mainloop()
