import tests.data as sample
import impact
import unittest.mock as mock
import stackapi  # noqa


class TestFetchUserQuestions:

    def test_01_no_questions(self):
        with mock.patch('stackapi.StackAPI', autospec=True) as StackAPIMock:
            api = StackAPIMock.return_value
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
