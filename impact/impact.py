from typing import Any, Optional
import stackapi
import collections
from impact import answered


class StackExchangeImpact:

    def __init__(self, site='stackoverflow', api_key=None, api: Optional[Any] = None):
        if api is None:
            self.api = stackapi.StackAPI(site, key=api_key)
        else:
            self.api = api

        self._questions_asked_views = collections.defaultdict(int)
        self._answered_questions: dict[int, answered.Question] = {}

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
                question = answered.Question(answer)
            except answered.DiscardQuestion:
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

    def _calculate_impact(self):

        result = sum(self._questions_asked_views.values())

        result += sum(question.views for question in self._answered_questions.values() if question.useful)

        return result

    def calculate(self, user_id: int):

        self._fetch_user_questions(user_id)
        self._fetch_user_answers(user_id)
        self._fetch_answered_questions()
        self._fetch_question_answers()

        result = self._calculate_impact()

        return result
