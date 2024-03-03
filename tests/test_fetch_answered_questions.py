import tests.data as sample
import impact
import impact.answered as answered
import unittest.mock as mock
from tests.fixtures import api


class TestFetchAnsweredQuestions:

    def test_01_no_questions(self, api: mock.Mock):

        # Some data expected not to be retrieved at all
        api.fetch.return_value = {
            'backoff': 0, 'has_more': False, 'page': 1, 'quota_max': 300, 'quota_remaining': 297, 'total': 0,
            'items': [
                {'tags': ['python', 'plotly-dash'],
                 'owner': {'account_id': 16027765, 'reputation': 35, 'user_id': 20091272, 'user_type': 'registered',
                           'profile_image': 'https://graph.facebook.com/2170798369684006/picture?type=large',
                           'display_name': 'Mike  Lvov', 'link': 'https://stackoverflow.com/users/20091272/mike-lvov'},
                 'is_answered': True, 'view_count': 40, 'accepted_answer_id': 77146201, 'answer_count': 1, 'score': 1,
                 'last_activity_date': 1695248500, 'creation_date': 1694872179, 'question_id': 77118048,
                 'content_license': 'CC BY-SA 4.0',
                 'link': 'https://stackoverflow.com/questions/77118048/hiding-dynamically-updated-blocks',
                 'title': 'Hiding dynamically updated blocks'},
                {'tags': ['python', 'flask'],
                 'owner': {'account_id': 4641459, 'reputation': 77, 'user_id': 3761178, 'user_type': 'registered',
                           'profile_image': 'https://graph.facebook.com/1447291475/picture?type=large',
                           'display_name': 'Sim', 'link': 'https://stackoverflow.com/users/3761178/sim'},
                 'is_answered': True, 'view_count': 45,
                 'accepted_answer_id': 77123424, 'answer_count': 1,
                 'score': 0, 'last_activity_date': 1695170374,
                 'creation_date': 1694864376,
                 'last_edit_date': 1695170374, 'question_id': 77117609,
                 'content_license': 'CC BY-SA 4.0',
                 'link': 'https://stackoverflow.com/questions/77117609/flask-decorator-not-properly-applied',
                 'title': 'Flask decorator not properly applied'},
                {'tags': ['python', 'pdf', 'extract', 'pdfminer', 'pdfminersix'],
                 'owner': {'account_id': 3592325, 'reputation': 9052, 'user_id': 2998077, 'user_type': 'registered',
                           'accept_rate': 95, 'profile_image': 'https://i.stack.imgur.com/F7irZ.png?s=256&g=1',
                           'display_name': 'Mark K', 'link': 'https://stackoverflow.com/users/2998077/mark-k'},
                 'is_answered': True, 'view_count': 41, 'accepted_answer_id': 77110938, 'answer_count': 1, 'score': 1,
                 'last_activity_date': 1694804187, 'creation_date': 1694766055, 'last_edit_date': 1694804187,
                 'question_id': 77110748, 'content_license': 'CC BY-SA 4.0',
                 'link': 'https://stackoverflow.com/questions/77110748/to-extract-texts-in-selected-pages-from-pdf',
                 'title': 'To extract texts in selected page(s) from PDF'}
            ]}

        instance = impact.StackExchangeImpact(api=api)
        instance._answered_questions = {}
        questions_to_inspect = instance._fetch_answered_questions()

        assert len(instance._answered_questions) == 0
        assert len(questions_to_inspect) == 0

    def test_02_already_useful(self, api: mock.Mock):

        api.fetch.return_value = {
            'backoff': 0, 'has_more': False, 'page': 1, 'quota_max': 300, 'quota_remaining': 297, 'total': 0,
            'items': [{
                'view_count': sample.VIEWS,
                'answer_count': 1,
                'question_id': sample.QUESTION_ID}]
        }

        instance = impact.StackExchangeImpact(api=api)
        instance._answered_questions[sample.QUESTION_ID] = sample.question(**{
                'is_accepted': True,
                'score': 0,
                'answer_id': sample.ANSWER_ID,
                'question_id': sample.QUESTION_ID})

        questions_to_inspect = instance._fetch_answered_questions()

        assert len(questions_to_inspect) == 0
        assert len(instance._answered_questions) == 1
        assert instance._answered_questions[sample.QUESTION_ID].views == sample.VIEWS
        assert instance._answered_questions[sample.QUESTION_ID].useful
        assert instance._answered_questions[sample.QUESTION_ID].inspect_answers is False

    def test_03_top_answer(self, api: mock.Mock):

        api.fetch.return_value = {
            'backoff': 0, 'has_more': False, 'page': 1, 'quota_max': 300, 'quota_remaining': 297, 'total': 0,
            'items': [{
                'view_count': sample.VIEWS,
                'answer_count': 1,
                'question_id': sample.QUESTION_ID}]
        }

        instance = impact.StackExchangeImpact(api=api)
        instance._answered_questions[sample.QUESTION_ID] = sample.question(**{
                'is_accepted': False,
                'score': 1,
                'answer_id': sample.ANSWER_ID,
                'question_id': sample.QUESTION_ID})

        questions_to_inspect = instance._fetch_answered_questions()

        assert len(questions_to_inspect) == 0
        assert len(instance._answered_questions) == 1
        assert instance._answered_questions[sample.QUESTION_ID].views == sample.VIEWS
        assert instance._answered_questions[sample.QUESTION_ID].useful
        assert instance._answered_questions[sample.QUESTION_ID].inspect_answers is False

    def test_04_many_answers(self, api: mock.Mock):

        api.fetch.return_value = {
            'backoff': 0, 'has_more': False, 'page': 1, 'quota_max': 300, 'quota_remaining': 297, 'total': 0,
            'items': [{
                'view_count': sample.VIEWS,
                'answer_count': answered.TOP_ANSWERS + 1,
                'question_id': sample.QUESTION_ID}]
        }

        instance = impact.StackExchangeImpact(api=api)
        instance._answered_questions[sample.QUESTION_ID] = sample.question(**{
                'is_accepted': False,
                'score': 1,
                'answer_id': sample.ANSWER_ID,
                'question_id': sample.QUESTION_ID})

        questions_to_inspect = instance._fetch_answered_questions()

        assert len(questions_to_inspect) == 1
        assert len(instance._answered_questions) == 1
        assert instance._answered_questions[sample.QUESTION_ID].views == sample.VIEWS
        assert instance._answered_questions[sample.QUESTION_ID].useful is False
        assert instance._answered_questions[sample.QUESTION_ID].inspect_answers is True

    def test_05_pages(self, api: mock.Mock):

        times = 3

        api.page_size = 1
        api.fetch.return_value = {
            'backoff': 0, 'has_more': False, 'page': 1, 'quota_max': 300, 'quota_remaining': 297, 'total': 0,
            'items': []}

        instance = impact.StackExchangeImpact(api=api)

        for offset in range(times):
            instance._answered_questions[sample.QUESTION_ID + offset] = sample.question(**{
                'is_accepted': False,
                'score': 1,
                'answer_id': sample.ANSWER_ID + offset,
                'question_id': sample.QUESTION_ID + offset})

        instance._fetch_answered_questions()

        assert api.fetch.call_count == times
