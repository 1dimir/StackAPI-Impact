import pytest
from impact import answered
from tests.fixtures import (regular_answered_question, accepted_answered_question)


class TestAnsweredQuestion:

    def test_01_init_no_score(self):

        with pytest.raises(ValueError,
                           match="Cannot retrieve the score of the answer data"):
            _ = answered.Question({})

    def test_02_init_str_score(self):

        with pytest.raises(ValueError,
                           match="Cannot retrieve the score of the answer data"):
            _ = answered.Question(
                {'score': "ok"})

    def test_03_init_zero_score(self):

        with pytest.raises(answered.DiscardQuestion):
            _ = answered.Question(
                {'score': 0})

    def test_04_init_negative_score(self):

        with pytest.raises(answered.DiscardQuestion):
            _ = answered.Question(
                {'score': -3})

    def test_05_no_question_id(self):

        with pytest.raises(ValueError,
                           match="Cannot retrieve question_id of the answer"):
            _ = answered.Question(
                {'score': 1})

    def test_06_init_str_question_id(self):

        with pytest.raises(ValueError,
                           match="Cannot retrieve question_id of the answer"):
            _ = answered.Question(
                {'score': 1,
                 'question_id': "c9dafe9e-9233-46d5-afc3-0628255a82d2"})

    def test_07_init_no_is_accepted(self):

        with pytest.raises(ValueError,
                           match="Cannot identify if the answer was accepted"):
            _ = answered.Question(
                {'score': 1,
                 'question_id': 1})

    def test_08_init_accepted(self):

        score = 1

        question = answered.Question({
            'score': score,
            'question_id': 1,
            'is_accepted': True
        })

        assert question.user_score == score
        assert question.useful is True
        assert question.inspect_answers is False
        assert question.views == 0
        assert question.answer_count == 0
        assert question.total_score == 0
        assert question.top_scores == []

    def test_09_init_high_score(self):
        score = 10

        question = answered.Question({
            'score': score,
            'question_id': 1,
            'is_accepted': False
        })

        assert question.user_score == score
        assert question.useful is True
        assert question.inspect_answers is False
        assert question.views == 0
        assert question.answer_count == 0
        assert question.total_score == 0
        assert question.top_scores == []

    def test_10_init_accepted_high_score(self):
        score = 10

        question = answered.Question({
            'score': score,
            'question_id': 1,
            'is_accepted': True
        })

        assert question.user_score == score
        assert question.useful is True
        assert question.inspect_answers is False
        assert question.views == 0
        assert question.answer_count == 0
        assert question.total_score == 0
        assert question.top_scores == []

    def test_11_init_inspect_answers(self):
        score = 2

        question = answered.Question({
            'score': score,
            'question_id': 1,
            'is_accepted': False
        })

        assert question.user_score == score
        assert question.useful is False
        assert question.inspect_answers is True
        assert question.views == 0
        assert question.answer_count == 0
        assert question.total_score == 0
        assert question.top_scores == []

    def test_12_update_no_view_count(self, regular_answered_question):
        with pytest.raises(ValueError,
                           match="Cannot retrieve view_count of the question"):
            regular_answered_question.update({})

    def test_13_update_str_view_count(self, regular_answered_question):
        with pytest.raises(ValueError,
                           match="Cannot retrieve view_count of the question"):
            regular_answered_question.update(
                {'view_count': "12K"})

    def test_14_update_no_answer_count(self, regular_answered_question):
        with pytest.raises(ValueError,
                           match="Cannot retrieve the number of answers for the question"):
            regular_answered_question.update(
                {'view_count': 42})

    def test_15_update_none_answer_count(self, regular_answered_question):
        with pytest.raises(ValueError,
                           match="Cannot retrieve the number of answers for the question"):
            regular_answered_question.update(
                {'view_count': 42,
                 'answer_count': None})

    def test_16_update_str_answer_count(self, regular_answered_question):
        with pytest.raises(ValueError,
                           match="Cannot retrieve the number of answers for the question"):
            regular_answered_question.update(
                {'view_count': 42,
                 'answer_count': "one"})

    def test_17_update_top_answer(self, regular_answered_question):
        views = 1024
        answer_count = 2

        regular_answered_question.update(
            {'view_count': views,
             'answer_count': answer_count})

        assert regular_answered_question.views == views
        assert regular_answered_question.answer_count == answer_count
        assert regular_answered_question.useful is True
        assert regular_answered_question.inspect_answers is False

    def test_18_update_many_answers(self, regular_answered_question):
        views = 1024
        answer_count = 12

        regular_answered_question.update(
            {'view_count': views,
             'answer_count': answer_count})

        assert regular_answered_question.views == views
        assert regular_answered_question.answer_count == answer_count
        assert regular_answered_question.useful is False
        assert regular_answered_question.inspect_answers is True

    def test_19_update_already_useful(self, accepted_answered_question):
        views = 1024
        answer_count = 12

        accepted_answered_question.update(
            {'view_count': views,
             'answer_count': answer_count})

        assert accepted_answered_question.views == views
        assert accepted_answered_question.answer_count == answer_count
        assert accepted_answered_question.useful is True
        assert accepted_answered_question.inspect_answers is False