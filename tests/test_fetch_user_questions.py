import tests.data as sample
import impact
import unittest.mock as mock
from tests.fixtures import api
import stackapi  # noqa
import random


class TestFetchUserQuestions:

    def test_01_no_questions(self, api: mock.Mock):
        api.fetch.return_value = {
            'backoff': 0,
            'has_more': False,
            'items': [],
            'page': 1,
            'quota_max': 300,
            'quota_remaining': 296,
            'total': 0}

        instance = impact.StackExchangeImpact(api=api)
        instance._fetch_user_questions(sample.USER_ID)

        assert len(instance._questions_asked_views) == 0

    def test_02_single_question(self, api: mock.Mock):

        api.fetch.return_value = {
            'backoff': 0,
            'has_more': False,
            'items': [
                {'tags': ['test'],
                 'owner': {},
                 'is_answered': True,
                 'view_count': sample.VIEWS,
                 'answer_count': 1,
                 'score': -1,
                 'last_activity_date': 1708449073,
                 'creation_date': 1708358751,
                 'last_edit_date': 1708449073,
                 'question_id': sample.QUESTION_ID,
                 'content_license': 'CC BY-SA 4.0',
                 'link': '',
                 'title': 'Sample title'
                 }],
            'page': 1,
            'quota_max': 300,
            'quota_remaining': 296,
            'total': 0}

        instance = impact.StackExchangeImpact(api=api)
        instance._fetch_user_questions(sample.USER_ID)

        assert len(instance._questions_asked_views) == 1
        assert sample.QUESTION_ID in instance._questions_asked_views
        assert instance._questions_asked_views[sample.QUESTION_ID] == sample.VIEWS

    def test_03_several_questions(self, api: mock.Mock):

        total = 10
        questions = list(range(total))
        views = [random.randrange(1, 1000) for _ in range(total)]

        api.fetch.return_value = {
            'backoff': 0,
            'has_more': False,
            'items': [{'view_count': views[index], 'question_id': questions[index]} for index in range(total)],
            'page': 1,
            'quota_max': 300,
            'quota_remaining': 296,
            'total': 0}

        instance = impact.StackExchangeImpact(api=api)
        instance._fetch_user_questions(sample.USER_ID)

        assert len(instance._questions_asked_views) == total

        for question_id, view_count in zip(questions, views):
            assert question_id in instance._questions_asked_views
            assert instance._questions_asked_views[question_id] == view_count
