class Question:
    def __init__(self, question_text, options, correct_answer, difficulty, topic):
        self.question_text = question_text
        self.options = options
        self.correct_answer = correct_answer
        self.difficulty = difficulty
        self.topic = topic

    def is_correct(self, selected_option):
        return selected_option == self.correct_answer
