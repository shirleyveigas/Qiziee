import tkinter as tk
import time
from tkinter import messagebox
from results import save_result

TIMER_DURATION = 30  

def get_user_details():
    input_window = tk.Tk()
    input_window.title("Enter Details")
    input_window.geometry("300x150")
    input_window.resizable(False, False)
    tk.Label(input_window, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    name_entry = tk.Entry(input_window, width=25)
    name_entry.grid(row=0, column=1)
    tk.Label(input_window, text="Branch:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    branch_entry = tk.Entry(input_window, width=25)
    branch_entry.grid(row=1, column=1)
    user_data = {"name": None, "branch": None}

    def submit():
        user_data["name"] = name_entry.get()
        user_data["branch"] = branch_entry.get()
        input_window.destroy()

    submit_btn = tk.Button(input_window, text="Continue", command=submit)
    submit_btn.grid(row=2, column=0, columnspan=2, pady=15)
    input_window.mainloop()
    return user_data["name"], user_data["branch"]

class QuizGUI:
    def __init__(self, quiz):
        self.quiz = quiz
        self.name, self.branch = get_user_details()
        self.result_shown = False
        self.timer_running = False
        self.timer_id = None
        self.show_welcome_screen()

    def show_welcome_screen(self):
        self.welcome = tk.Tk()
        self.welcome.title("Welcome to Quiz")
        self.welcome.geometry("500x300")
        self.welcome.resizable(False, False)
        title = tk.Label(self.welcome, text="🧠 ROOT Quiz App", font=("Arial", 20, "bold"))
        title.pack(pady=10)
        user_info = tk.Label(self.welcome, text=f"Welcome, {self.name} ({self.branch})", font=("Arial", 12))
        user_info.pack(pady=5)
        instructions = tk.Label(
            self.welcome,
            text=f"📋 Instructions:\n- You will be asked multiple choice questions.\n- Each question has a {TIMER_DURATION}-second timer.\n- Click 'Next' to continue.\n- Your score will be saved after completion.",
            font=("Arial", 11),
            justify="left"
        )
        instructions.pack(pady=10)
        start_button = tk.Button(self.welcome, text="Start Quiz", font=("Arial", 12), command=self.start_quiz)
        start_button.pack(pady=15)
        self.welcome.mainloop()

    def start_quiz(self):
        self.welcome.destroy()
        self.window = tk.Tk()
        self.window.title("R00T Quiz")
        self.window.geometry("600x500")
        self.window.configure(bg="#eaf6ff")
        self.time_left = TIMER_DURATION
        self.timer_label = tk.Label(
            self.window,
            text=f"⏳ Time left: {self.time_left}s",
            font=("Helvetica", 12, "bold"),
            fg="#d32f2f",
            bg="#eaf6ff"
        )
        self.timer_label.pack(pady=10)
        self.question_label = tk.Label(
            self.window,
            text="",
            wraplength=500,
            font=("Helvetica", 14, "bold"),
            fg="#263238",
            bg="#eaf6ff"
        )
        self.question_label.pack(pady=20)
        self.var = tk.StringVar()
        self.options = []
        for _ in range(4):
            btn = tk.Radiobutton(
                self.window,
                text="",
                variable=self.var,
                value="",
                font=("Helvetica", 12),
                fg="#000000",
                bg="#ffffff",
                selectcolor="#bbdefb",
                activebackground="#e3f2fd",
                anchor="w",
                padx=10,
                relief="groove",
                borderwidth=1,
                indicatoron=0,
                height=2,
                width=40
            )
            btn.pack(pady=5)
            self.options.append(btn)
        self.feedback_label = tk.Label(
            self.window,
            text="",
            font=("Helvetica", 12, "bold"),
            bg="#eaf6ff"
        )
        self.feedback_label.pack(pady=10)
        self.next_button = tk.Button(
            self.window,
            text="Next ▶",
            command=self.next_question,
            font=("Helvetica", 12, "bold"),
            bg="#1976d2",
            fg="white",
            activebackground="#1565c0",
            relief="flat",
            padx=15,
            pady=5,
            cursor="hand2"
        )
        self.next_button.pack(pady=20)
        self.load_question()
        self.window.mainloop()

    def load_question(self):
        if self.quiz.is_finished():
            self.show_result()
            return
        self.feedback_label.config(text="")
        question = self.quiz.get_current_question()
        if question:
            self.question_label.config(text=question.question_text)
            self.var.set(None)
            for i, option in enumerate(question.options):
                self.options[i].config(text=option, value=option)
            self.time_left = TIMER_DURATION
            self.stop_timer()  # Stop any existing timer
            self.update_timer()

    def stop_timer(self):
        if self.timer_id is not None:
            self.window.after_cancel(self.timer_id)
            self.timer_id = None
            self.timer_running = False

    def update_timer(self):
        if self.quiz.is_finished() or self.result_shown:
            return

        self.timer_label.config(text=f"Time left: {self.time_left}s")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.window.after(1000, self.update_timer)
            self.timer_running = True
        else:
            self.timer_running = False
            self.feedback_label.config(text="⏱️ Time's up! Moving to next question...", fg="red")
            self.quiz.answer_current_question("")
            self.window.after(1500, self.load_question)

    def next_question(self):
        if self.quiz.is_finished():
            self.show_result()
            return

        selected = self.var.get()
        if not selected:
            self.feedback_label.config(text="⚠️ Please select an option.", fg="orange")
            return

        current_question = self.quiz.get_current_question()
        correct_answer = current_question.correct_answer
        self.quiz.answer_current_question(selected)

        if selected == correct_answer:
            self.feedback_label.config(text="✅ Correct!", fg="green")
        else:
            self.feedback_label.config(
                text=f"❌ Wrong! Correct Answer: {correct_answer}", fg="red"
            )

        self.window.after(1500, self.load_question)

    def show_result(self):
        if self.result_shown:
            return
        self.result_shown = True
        save_result(self.name, self.branch, self.quiz.score, len(self.quiz.questions))
        messagebox.showinfo("Result Saved", f"{self.name} ({self.branch}), your score is {self.quiz.score}/{len(self.quiz.questions)}")
        self.window.destroy()
