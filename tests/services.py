class TestService:

    @staticmethod
    def calculate_score(student_answers, correct_answers):

        score = 0

        for q in correct_answers:

            if student_answers[q] == correct_answers[q]:

                score += 1

        return score