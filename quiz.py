import json
from questions import Question

class Quiz:
    def __init__(self, question_file):
        self.questions = self.load_questions(question_file)
        self.current_index = 0
        self.score = 0

    def load_questions(self, filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
        questions = []
        for item in data:
            q = Question(
                item['question_text'],
                item['options'],
                item['correct_answer'],
                item['difficulty'],
                item['topic']
            )
            questions.append(q)
            
        return questions

    def get_current_question(self):
        if self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None

    def answer_current_question(self, selected_option):
        current = self.get_current_question()
        if current and current.is_correct(selected_option):
            self.score += 1
        self.current_index += 1

    def is_finished(self):
        return self.current_index >= len(self.questions)
