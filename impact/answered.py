import heapq


TOP_ANSWERS: int = 3
SCORE_THRESHOLD: float = 0.2


class DiscardQuestion(Exception):
    pass


class Question:

    def __init__(self, answer: dict):

        try:
            answer_score = int(answer['score'])
        except (TypeError, KeyError):
            raise ValueError("Cannot retrieve the score of the answer data")

        if answer_score <= 0:
            raise DiscardQuestion()

        try:
            self.id: int = int(answer['question_id'])
        except (TypeError, KeyError):
            raise ValueError("Cannot retrieve question_id of the answer")

        try:
            accepted = answer['is_accepted'] is True
        except (TypeError, KeyError):
            raise ValueError("Cannot identify if the answer was accepted")

        self.user_score: int = answer_score
        self.useful: bool = accepted and self.user_score >= 5
        self.inspect_answers: bool = not self.useful

        self.views: int = 0
        self.answer_count: int = 0
        self.total_score: int = 0
        self.top_scores: list[int] = []

    def update(self, question: dict):

        try:
            self.views = question['view_count']
        except (TypeError, KeyError):
            raise ValueError("Cannot retrieve view_count of the question")

        try:
            self.answer_count = question['answer_count']
        except (TypeError, KeyError):
            raise ValueError("Cannot retrieve the number of answers for the question")

        self.useful = self.useful or self.answer_count <= 3
        self.inspect_answers = not self.useful

    def inspect_answer(self, answer: dict):

        try:
            score = int(answer['score'])
        except (TypeError, KeyError):
            raise ValueError("Cannot retrieve the score of answers for the question")

        if score <= 0:
            return

        self.total_score += score

        heapq.heappush(self.top_scores, score)
        if len(self.top_scores) > TOP_ANSWERS:
            heapq.heappop(self.top_scores)

        if not self.inspect_answers:
            return

        self.useful = max(SCORE_THRESHOLD * self.total_score, min(self.top_scores)) <= self.user_score
