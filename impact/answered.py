import heapq


TOP_ANSWERS: int = 3
SCORE_THRESHOLD: float = 0.2
HALF_NICE = 5


class DiscardQuestion(Exception):
    pass


class Question:

    def __init__(self, answer: dict):

        try:
            answer_score = int(answer['score'])
        except (TypeError, ValueError, KeyError) as exception:
            raise ValueError("Cannot retrieve the score of the answer data") from exception

        try:
            self.id: int = int(answer['question_id'])
        except (TypeError, ValueError, KeyError) as exception:
            raise ValueError("Cannot retrieve question_id of the answer") from exception

        try:
            accepted = answer['is_accepted'] is True
        except (TypeError, KeyError) as exception:
            raise ValueError("Cannot identify if the answer was accepted") from exception

        # Zero score accepted answers are useful, examples:
        #   user:23478142, user:3275112, user:8357
        # Also negative score accepted answers are useful too, example:
        #   user:23167706
        if answer_score <= 0 and not accepted:
            raise DiscardQuestion()

        self.user_score: int = answer_score
        self.useful: bool = accepted or self.user_score >= HALF_NICE
        self.inspect_answers: bool = not self.useful

        self.views: int = 0
        self.answer_count: int = 0
        self.total_score: int = 0
        self.top_scores: list[int] = []

    def update(self, question: dict):

        try:
            self.views = int(question['view_count'])
        except (TypeError, ValueError, KeyError) as exception:
            raise ValueError("Cannot retrieve view_count of the question") from exception

        try:
            self.answer_count = int(question['answer_count'])
        except (TypeError, ValueError, KeyError) as exception:
            raise ValueError("Cannot retrieve the number of answers for the question") from exception

        self.useful = self.useful or self.answer_count <= TOP_ANSWERS
        self.inspect_answers = not self.useful

    def inspect_answer(self, answer: dict):

        if not self.inspect_answers:
            return

        try:
            score = int(answer['score'])
        except (TypeError, KeyError) as exception:
            raise ValueError("Cannot retrieve the score of answers for the question") from exception

        if score <= 0:
            return

        self.total_score += score

        heapq.heappush(self.top_scores, score)
        if len(self.top_scores) > TOP_ANSWERS:
            heapq.heappop(self.top_scores)

    def evaluate_answers(self):

        if not self.inspect_answers:
            return

        self.useful = min(SCORE_THRESHOLD * self.total_score, *self.top_scores) <= self.user_score
