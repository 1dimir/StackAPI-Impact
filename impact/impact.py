import stackapi
import collections
import heapq


# We need mutable types
VIEWS = 0
SCORE = 1
OWNER = 2
QUESTION = 3
ANSWERS = 3
RANK = 4


class ImpactCalculator:

    def __init__(self, site='stackoverflow', api_key=None):
        self.api = stackapi.StackAPI(site, key=api_key)

        self._user_questions = collections.defaultdict(self.question_factory)
        self._user_answers = collections.defaultdict(self.answer_factory)
        self._answered_questions_ids = collections.defaultdict(bool)
        self._answered_questions = collections.defaultdict(self.question_factory)
        self._ranking_questions_ids = []
        self._user_id = 0

    def reset(self):
        self._user_questions.clear()
        self._user_answers.clear()
        self._answered_questions.clear()
        self._answered_questions_ids.clear()
        self._ranking_questions_ids = []
        self._user_id = 0

    @staticmethod
    def question_factory():
        return [
            0,  # VIEWS
            0,  # SCORES
            None,  # OWNER
            []  # ANSWERS
        ]

    @staticmethod
    def answer_factory():
        return [
            0,  # VIEWS
            0,  # SCORE
            None,  # OWNER
            None  # QUESTION
        ]

    @staticmethod
    def answered_question_factory():
        return [
            0,  # VIEWS
            None  # QUESTION
        ]

    def _fetch_user_questions(self, user_id):

        response = self.api.fetch('users/{ids}/questions', ids=user_id)
        for question in response['items']:
            self._user_questions[question['question_id']] = [
                question['view_count'],
                question['score'],
                question['owner']['user_id']]

    def _fetch_user_answers(self, user_id):

        response = self.api.fetch('users/{ids}/answers', ids=user_id)
        for answer in response['items']:
            if answer['score'] <= 0:
                continue

            if answer['question_id'] in self._user_questions:
                continue

            get_rank = not answer['is_accepted'] and (answer['score'] < 5)

            self._user_answers[answer['answer_id']] = [
                0,
                answer['score'],
                answer['owner']['user_id'],
                answer['question_id'],
                get_rank]

            self._answered_questions_ids[answer['question_id']] = get_rank

    def _fetch_answered_questions(self):

        total = len(self._answered_questions_ids)
        keys = list(self._answered_questions_ids.keys())

        for split in range(0, total, self.api.page_size):
            response = self.api.fetch(
                'questions/{ids}',
                ids=keys[split:split + self.api.page_size])

            for question in response['items']:
                question_id = question['question_id']

                self._answered_questions[question_id] = [
                    question['view_count'],
                    0,
                    question['owner']['user_id'],
                    []]

                check_rank = self._answered_questions_ids[question_id]
                check_rank = check_rank and question['answer_count'] > 3

                if check_rank:
                    self._ranking_questions_ids.append(question_id)

    def _fetch_question_answers(self):
        total = len(self._ranking_questions_ids)

        for split in range(0, total, self.api.page_size):
            response = self.api.fetch('questions/{ids}/answers',
                                      ids=self._ranking_questions_ids[
                                          split:split + self.api.page_size])

            for answer in response['items']:
                if answer['score'] <= 0:
                    continue

                question_id = answer['question_id']
                self._answered_questions[question_id][SCORE] += answer['score']

                heapq.heappush(
                    self._answered_questions[question_id][ANSWERS],
                    answer['score'])
                if len(self._answered_questions[question_id][ANSWERS]) > 3:
                    heapq.heappop(
                        self._answered_questions[question_id][ANSWERS])

    def impact(self, user_id: int):

        self._fetch_user_questions(user_id)
        self._fetch_user_answers(user_id)
        self._fetch_answered_questions()
        self._fetch_question_answers()

        result = sum(question[VIEWS] for question in self._user_questions.values())

        for answer in self._user_answers.values():
            question_id = answer[QUESTION]
            question = self._answered_questions[question_id]
            if question[ANSWERS]:
                min_score = min(question[ANSWERS])
                if (answer[SCORE] < min_score and answer[SCORE] < 0.2 *
                        question[SCORE]):
                    continue
            result += self._answered_questions[question_id][VIEWS]

        return result
