from quiz import Quiz
from gui import QuizGUI

if __name__ == "__main__":
    quiz = Quiz("question.json")
    QuizGUI(quiz)
