import heapq


TOP_ANSWERS = 3
SCORE_THRESHOLD = 0.2


class ParsingError(Exception):
    pass


class DiscardQuestion(Exception):
    pass


class Question:

    def __init__(self, answer: dict):

        if answer['score'] <= 0:
            raise DiscardQuestion()

        try:
            self.id = answer['question_id']
        except (TypeError, KeyError):
            raise ParsingError()

        try:
            self.user_score = answer['score']
        except (TypeError, KeyError):
            raise ParsingError()

        self.views: int = 0

        try:
            accepted = answer['is_accepted'] is True
        except (TypeError, KeyError):
            raise ParsingError()

        self.useful = accepted and self.user_score >= 5
        self.inspect_answers = not self.useful
        self.answer_count = 0
        self.total_score = 0
        self.top_scores = []

    def update(self, question: dict):

        try:
            self.views = question['view_count']
        except (TypeError, KeyError):
            raise ParsingError()

        try:
            self.answer_count = question['answer_count']
        except (TypeError, KeyError):
            raise ParsingError()

        self.useful = self.useful or self.answer_count <= 3
        self.inspect_answers = not self.useful

    def inspect_answer(self, answer: dict):

        try:
            score = answer['score']
        except (TypeError, KeyError):
            raise ParsingError()

        if score <= 0:
            return

        self.total_score += score

        heapq.heappush(self.top_scores, score)
        if len(self.top_scores) > TOP_ANSWERS:
            heapq.heappop(self.top_scores)

        if not self.inspect_answers:
            return

        self.useful = max(min(self.top_scores), self.total_score * SCORE_THRESHOLD) <= self.user_score
