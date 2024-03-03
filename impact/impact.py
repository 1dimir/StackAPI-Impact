from typing import Any, Optional, DefaultDict
import stackapi
import collections
from impact import answered


class StackExchangeImpact:

    def __init__(self, site='stackoverflow', api_key=None, api: Optional[Any] = None, keep_cache: bool = False):
        if api is None:
            self.api: stackapi.StackAPI = stackapi.StackAPI(site, key=api_key)
        else:
            self.api: Any = api

        self._keep_cache: bool = keep_cache
        self._questions_asked_views: DefaultDict[int, int] = collections.defaultdict(int)
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

        """
        Populates collection of answered question with question-related information.
        Returns a list of question ids that require answer inspection to determine answer usefulness.
        """

        total = len(self._answered_questions)
        question_ids = list(self._answered_questions.keys())
        questions_to_inspect = []

        for split in range(0, total, self.api.page_size):
            response = self.api.fetch(
                'questions/{ids}',
                ids=question_ids[split:split + self.api.page_size])

            for question in response['items']:
                question_id = question['question_id']

                self._answered_questions[question_id].update(question)
                if self._answered_questions[question_id].inspect_answers:
                    questions_to_inspect.append(question_id)

        return questions_to_inspect

    def _fetch_question_answers(self, question_ids: Optional[list] = None):

        if question_ids is None:
            question_ids = [question.id for question in self._answered_questions.values() if question.inspect_answers]

        total = len(question_ids)

        for split in range(0, total, self.api.page_size):
            response = self.api.fetch('questions/{ids}/answers',
                                      ids=question_ids[split:split + self.api.page_size])

            for answer in response['items']:
                question_id = answer['question_id']

                try:
                    self._answered_questions[question_id].inspect_answer(answer)
                except KeyError:
                    pass  # unexpected question, skip it

    def _evaluate_answers(self, question_ids: Optional[list] = None):

        if question_ids is None:
            for question in self._answered_questions.values():
                question.evaluate_answers()  # inspect_answers is checked inside
            return

        for question_id in question_ids:
            try:
                self._answered_questions[question_id].evaluate_answers()
            except KeyError:
                pass  # unexpected question, skip it

    def _calculate_impact(self):

        result = sum(self._questions_asked_views.values())

        result += sum(question.views for question in self._answered_questions.values() if question.useful)

        return result

    def calculate(self, user_id: int):

        self._fetch_user_questions(user_id)
        self._fetch_user_answers(user_id)
        question_ids = self._fetch_answered_questions()
        self._fetch_question_answers(question_ids)
        self._evaluate_answers(question_ids)

        result = self._calculate_impact()

        return result
