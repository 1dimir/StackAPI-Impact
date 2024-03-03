import tests.data as sample
import impact
import impact.answered as answered
import unittest.mock as mock
from tests.fixtures import api


class TestFetchQuestionAnswers:

    def test_01_no_questions(self, api: mock.Mock):

        # Some data expected not to be retrieved at all
        api.fetch.return_value = {
            'backoff': 0, 'has_more': False, 'page': 1, 'quota_max': 300, 'quota_remaining': 297, 'total': 0,
            'items': []}

        instance = impact.StackExchangeImpact(api=api)
        instance._fetch_question_answers([])

        assert len(instance._answered_questions) == 0
        assert api.fetch.call_count == 0

    def test_02_already_useful(self, api: mock.Mock):

        # Some data expected not to be retrieved at all
        api.fetch.return_value = {
            'backoff': 0, 'has_more': False, 'page': 1, 'quota_max': 300, 'quota_remaining': 297, 'total': 0,
            'items': []}

        instance = impact.StackExchangeImpact(api=api)

        instance._answered_questions[sample.QUESTION_ID] = sample.question(**{
            'is_accepted': True,
            'score': 0,
            'useful': True,
            'inspect_answers': False,
            'answer_id': sample.ANSWER_ID,
            'question_id': sample.QUESTION_ID})

        instance._answered_questions[sample.QUESTION_ID + 1] = sample.question(**{
            'is_accepted': False,
            'score': sample.NICE_QUESTION_SCORE,
            'useful': True,
            'inspect_answers': False,
            'answer_id': sample.ANSWER_ID + 1,
            'question_id': sample.QUESTION_ID + 1})

        instance._answered_questions[sample.QUESTION_ID + 2] = sample.question(**{
            'is_accepted': False,
            'score': 1,
            'answer_count': answered.TOP_ANSWERS - 1,
            'useful': True,
            'inspect_answers': False,
            'answer_id': sample.ANSWER_ID + 2,
            'question_id': sample.QUESTION_ID + 2})

        instance._fetch_question_answers()

        assert api.fetch.call_count == 0
        assert all(question.useful for question in instance._answered_questions.values()) is True

    def test_03_unexpected_question(self, api: mock.Mock):

        # Some data expected not to be retrieved at all
        api.fetch.return_value = {
            'backoff': 0, 'has_more': False, 'page': 1, 'quota_max': 300, 'quota_remaining': 297, 'total': 0,
            'items': [
                {'score': 10,
                 'question_id': sample.QUESTION_ID}]}

        instance = impact.StackExchangeImpact(api=api)
        instance._fetch_question_answers([sample.QUESTION_ID])

        assert len(instance._answered_questions) == 0
        # and no exception...

    def test_04_inspect_answers(self, api: mock.Mock):

        # Some data expected not to be retrieved at all
        api.fetch.return_value = {
            'backoff': 0, 'has_more': False, 'page': 1, 'quota_max': 300, 'quota_remaining': 296, 'total': 0,
            'items': [
                {'owner': {'account_id': 27957901, 'reputation': 1012, 'user_id': 21350362, 'user_type': 'registered',
                           'profile_image': 'https://www.gravatar.com/avatar/6ae2aebb33a72b9986f409c63c736f89?s=256&d=identicon&r=PG',
                           'display_name': 'Dmitry', 'link': 'https://stackoverflow.com/users/21350362/dmitry'},
                 'is_accepted': False, 'score': 0, 'last_activity_date': 1702043964, 'last_edit_date': 1702043964,
                 'creation_date': 1702043523, 'answer_id': 77627047, 'question_id': sample.QUESTION_ID,
                 'content_license': 'CC BY-SA 4.0'},
                {'owner': {'account_id': 4485748, 'reputation': 2621, 'user_id': 3648453, 'user_type': 'registered',
                           'profile_image': 'https://i.stack.imgur.com/rikkW.jpg?s=256&g=1',
                           'display_name': 'wihlke', 'link': 'https://stackoverflow.com/users/3648453/wihlke'},
                 'is_accepted': False, 'score': 2, 'last_activity_date': 1678839296, 'last_edit_date': 1678839296,
                 'creation_date': 1647608331, 'answer_id': 71527398, 'question_id': sample.QUESTION_ID,
                 'content_license': 'CC BY-SA 4.0'},
                {'owner': {'account_id': 1618212, 'reputation': 3900, 'user_id': 1495323, 'user_type': 'registered',
                           'profile_image': 'https://www.gravatar.com/avatar/562b035c4de737014bdde5447893a9ab?s=256&d=identicon&r=PG',
                           'display_name': 'driedler', 'link': 'https://stackoverflow.com/users/1495323/driedler'},
                 'is_accepted': False, 'score': 24, 'last_activity_date': 1661784440, 'last_edit_date': 1661784440,
                 'creation_date': 1618258331, 'answer_id': 67065084, 'question_id': sample.QUESTION_ID,
                 'content_license': 'CC BY-SA 4.0'},
                {'owner': {'account_id': 25889302, 'reputation': 207, 'user_id': 19616939, 'user_type': 'registered',
                           'profile_image': 'https://www.gravatar.com/avatar/e0074f6a2144b196d2c1a5069a185ccd?s=256&d=identicon&r=PG',
                           'display_name': 'Gabriele Iannetti',
                           'link': 'https://stackoverflow.com/users/19616939/gabriele-iannetti'},
                 'is_accepted': False, 'score': -2, 'last_activity_date': 1659098244, 'creation_date': 1659098244,
                 'answer_id': 73166872, 'question_id': sample.QUESTION_ID, 'content_license': 'CC BY-SA 4.0'},
                {'owner': {'account_id': 1445661, 'reputation': 3926, 'user_id': 1364242, 'user_type': 'registered',
                           'accept_rate': 29, 'profile_image': 'https://i.stack.imgur.com/3zMnO.jpg?s=256&g=1',
                           'display_name': 'Jay M', 'link': 'https://stackoverflow.com/users/1364242/jay-m'},
                 'is_accepted': False, 'score': 1, 'last_activity_date': 1657788525, 'creation_date': 1657788525,
                 'answer_id': 72977762, 'question_id': sample.QUESTION_ID, 'content_license': 'CC BY-SA 4.0'},
                {'owner': {'account_id': 15795206, 'reputation': 623, 'user_id': 11397243, 'user_type': 'registered',
                           'profile_image': 'https://i.stack.imgur.com/4wWG0.jpg?s=256&g=1',
                           'display_name': 'snoopyjc', 'link': 'https://stackoverflow.com/users/11397243/snoopyjc'},
                 'is_accepted': False, 'score': 0, 'last_activity_date': 1650133928, 'creation_date': 1650133928,
                 'answer_id': 71896491, 'question_id': sample.QUESTION_ID, 'content_license': 'CC BY-SA 4.0'},
                {'owner': {'account_id': 3659569, 'reputation': 2102, 'user_id': 3049753, 'user_type': 'registered',
                           'accept_rate': 57, 'profile_image': 'https://i.stack.imgur.com/P4ed5.jpg?s=256&g=1',
                           'display_name': 'RedEyed', 'link': 'https://stackoverflow.com/users/3049753/redeyed'},
                 'is_accepted': False, 'score': 6, 'last_activity_date': 1645172768, 'creation_date': 1645172768,
                 'answer_id': sample.ANSWER_ID, 'question_id': sample.QUESTION_ID, 'content_license': 'CC BY-SA 4.0'},
                {'owner': {'account_id': 8605912, 'reputation': 3221, 'user_id': 6446053, 'user_type': 'registered',
                           'profile_image': 'https://i.stack.imgur.com/ITv5F.jpg?s=256&g=1', 'display_name': 'rpb',
                           'link': 'https://stackoverflow.com/users/6446053/rpb'}, 'is_accepted': False, 'score': 0,
                 'last_activity_date': 1638977269, 'creation_date': 1638977269, 'answer_id': 70277538,
                 'question_id': sample.QUESTION_ID, 'content_license': 'CC BY-SA 4.0'},
                {'owner': {'account_id': 37565, 'reputation': 78074, 'user_id': 107409, 'user_type': 'registered',
                           'accept_rate': 83, 'profile_image': 'https://i.stack.imgur.com/lGv9q.png?s=256&g=1',
                           'display_name': 'Contango', 'link': 'https://stackoverflow.com/users/107409/contango'},
                 'is_accepted': False, 'score': 0, 'last_activity_date': 1602515553, 'last_edit_date': 1602515553,
                 'creation_date': 1602514880, 'answer_id': 64320310, 'question_id': sample.QUESTION_ID,
                 'content_license': 'CC BY-SA 4.0'},
                {'owner': {'account_id': 1664820, 'reputation': 33011, 'user_id': 1532460, 'user_type': 'registered',
                           'accept_rate': 88,
                           'profile_image': 'https://www.gravatar.com/avatar/dc5b338bf194a9e117af20bd9b2e4edb?s=256&d=identicon&r=PG',
                           'display_name': 'awesoon', 'link': 'https://stackoverflow.com/users/1532460/awesoon'},
                 'is_accepted': True, 'score': 50, 'last_activity_date': 1469712305, 'creation_date': 1469712305,
                 'answer_id': 38637774, 'question_id': sample.QUESTION_ID, 'content_license': 'CC BY-SA 3.0'}]}

        instance = impact.StackExchangeImpact(api=api)

        instance._answered_questions[sample.QUESTION_ID] = sample.question(**{
            'is_accepted': False,
            'score': 6,
            'answer_count': 10,
            'inspect_answers': True,
            'answer_id': sample.ANSWER_ID,
            'question_id': sample.QUESTION_ID})

        instance._fetch_question_answers([sample.QUESTION_ID, sample.QUESTION_ID + 1])

        assert len(instance._answered_questions) == 1
        assert set(instance._answered_questions[sample.QUESTION_ID].top_scores) == {50, 24, 6}
        assert instance._answered_questions[sample.QUESTION_ID].total_score == 50 + 24 + 6 + 2 + 1
