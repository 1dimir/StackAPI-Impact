from typing import Dict
import stackapi
import collections
import heapq


TOP_ANSWERS = 3
SCORE_THRESHOLD = 0.2


class ParsingError(Exception):
    pass


class DiscardQuestion(Exception):
    pass


class AnsweredQuestion:

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


class ImpactCalculator:

    def __init__(self, site='stackoverflow', api_key=None):
        self.api = stackapi.StackAPI(site, key=api_key)

        self._questions_asked_views = collections.defaultdict(int)
        self._answered_questions: Dict[int, AnsweredQuestion] = {}

    def reset(self):
        self._questions_asked_views.clear()
        self._answered_questions.clear()

    def _fetch_user_questions(self, user_id):

        response = self.api.fetch('users/{ids}/questions', ids=user_id)
        for question in response['items']:
            self._questions_asked_views[question['question_id']] = question['view_count']

    def _fetch_user_answers(self, user_id):

        response = self.api.fetch('users/{ids}/answers', ids=user_id)
        for answer in response['items']:

            question_id = answer['question_id']

            if question_id in self._questions_asked_views:
                # already counted as a question
                continue

            try:
                question = AnsweredQuestion(answer)
            except DiscardQuestion:
                continue

            self._answered_questions[question_id] = question

    def _fetch_answered_questions(self):

        total = len(self._answered_questions)
        question_ids = list(self._answered_questions.keys())

        for split in range(0, total, self.api.page_size):
            response = self.api.fetch(
                'questions/{ids}',
                ids=question_ids[split:split + self.api.page_size])

            for question in response['items']:
                question_id = question['question_id']

                self._answered_questions[question_id].update(question)

    def _fetch_question_answers(self):

        question_ids = [question.id for question in self._answered_questions.values() if question.inspect_answers]
        total = len(question_ids)

        for split in range(0, total, self.api.page_size):
            response = self.api.fetch('questions/{ids}/answers',
                                      ids=question_ids[split:split + self.api.page_size])

            for answer in response['items']:
                question_id = answer['question_id']

                self._answered_questions[question_id].inspect_answer(answer)

    def impact(self, user_id: int):

        self._fetch_user_questions(user_id)
        self._fetch_user_answers(user_id)
        self._fetch_answered_questions()
        self._fetch_question_answers()

        result = sum(self._questions_asked_views.values())

        result += sum(question.views for question in self._answered_questions.values() if question.useful)

        return result
