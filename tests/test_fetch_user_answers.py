import tests.data as sample
import stackapi_impact as impact
import stackapi_impact.answered as answered
import unittest.mock as mock
from tests.fixtures import api
import random


class TestFetchUserAnswers:

    def test_01_no_answers(self, api: mock.Mock):

        api.fetch.return_value = {
            'backoff': 0,
            'has_more': False,
            'items': [],
            'page': 1,
            'quota_max': 300,
            'quota_remaining': 293,
            'total': 0}

        instance = impact.StackExchangeImpact(api=api)
        instance._fetch_user_answers(sample.USER_ID)

        assert len(instance._answered_questions) == 0

    def test_02_zero_score_answer(self, api: mock.Mock):

        api.fetch.return_value = {
            'backoff': 0, 'has_more': False, 'page': 1, 'quota_max': 300, 'quota_remaining': 292, 'total': 0,
            'items': [{
                'is_accepted': False,
                'score': 0,
                'answer_id': sample.ANSWER_ID,
                'question_id': sample.QUESTION_ID}]
        }

        instance = impact.StackExchangeImpact(api=api)
        instance._fetch_user_answers(sample.USER_ID)

        assert len(instance._answered_questions) == 0

    def test_03_zero_score_accepted_answer(self, api: mock.Mock):

        api.fetch.return_value = {
            'backoff': 0, 'has_more': False, 'page': 1, 'quota_max': 300, 'quota_remaining': 292, 'total': 0,
            'items': [{
                'is_accepted': True,
                'score': 0,
                'answer_id': sample.ANSWER_ID,
                'question_id': sample.QUESTION_ID}]
        }

        instance = impact.StackExchangeImpact(api=api)
        instance._fetch_user_answers(sample.USER_ID)

        assert len(instance._answered_questions) == 1
        assert sample.QUESTION_ID in instance._answered_questions
        assert isinstance(instance._answered_questions[sample.QUESTION_ID], answered.Question)
        assert instance._answered_questions[sample.QUESTION_ID].useful is True

    def test_04_nice_answer(self, api: mock.Mock):

        api.fetch.return_value = {
            'backoff': 0, 'has_more': False, 'page': 1, 'quota_max': 300, 'quota_remaining': 292, 'total': 0,
            'items': [{
                'is_accepted': False,
                'score': sample.NICE_QUESTION_SCORE,
                'answer_id': sample.ANSWER_ID,
                'question_id': sample.QUESTION_ID}]
        }

        instance = impact.StackExchangeImpact(api=api)
        instance._fetch_user_answers(sample.USER_ID)

        assert len(instance._answered_questions) == 1
        assert sample.QUESTION_ID in instance._answered_questions
        assert isinstance(instance._answered_questions[sample.QUESTION_ID], answered.Question)
        assert instance._answered_questions[sample.QUESTION_ID].useful is True

    def test_05_self_answers(self, api: mock.Mock):

        total = 4
        questions = [sample.QUESTION_ID + index for index in range(total)]
        answers = [sample.ANSWER_ID + index for index in range(total)]

        api.fetch.return_value = {
            'backoff': 0, 'has_more': False, 'page': 1, 'quota_max': 300, 'quota_remaining': 292, 'total': 0,
            'items': [{'is_accepted': False,
                       'score': sample.NICE_QUESTION_SCORE,
                       'answer_id': answers[0],
                       'question_id': questions[0]},
                      {'is_accepted': True,
                       'score': 0,
                       'answer_id': answers[1],
                       'question_id': questions[1]},
                      {'is_accepted': True,
                       'score': sample.NICE_QUESTION_SCORE,
                       'answer_id': answers[2],
                       'question_id': questions[2]},
                      {'is_accepted': True,
                       'score': -1,
                       'answer_id': answers[3],
                       'question_id': questions[3]}
                      ]
        }

        instance = impact.StackExchangeImpact(api=api)

        for question_id in questions:
            instance._questions_asked_views[question_id] = random.randrange(1, 10000)

        instance._fetch_user_answers(sample.USER_ID)

        assert len(instance._answered_questions) == 0

    def test_06_low_score_answer(self, api: mock.Mock):

        low_score = answered.HALF_NICE - 1

        api.fetch.return_value = {
            'backoff': 0, 'has_more': False, 'page': 1, 'quota_max': 300, 'quota_remaining': 292, 'total': 0,
            'items': [{
                'is_accepted': False,
                'score': low_score,
                'answer_id': sample.ANSWER_ID,
                'question_id': sample.QUESTION_ID}]
        }

        instance = impact.StackExchangeImpact(api=api)
        instance._fetch_user_answers(sample.USER_ID)

        assert len(instance._answered_questions) == 1
        assert sample.QUESTION_ID in instance._answered_questions
        assert isinstance(instance._answered_questions[sample.QUESTION_ID], answered.Question)
        assert instance._answered_questions[sample.QUESTION_ID].useful is False
