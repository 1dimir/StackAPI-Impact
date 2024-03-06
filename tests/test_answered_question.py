import pytest
from stackapi_impact import answered
import tests.data as sample
from tests.fixtures import (
    regular_answered_question, accepted_answered_question, answered_question_dont_inspect,
    answered_question_require_inspection)


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
                {'score': 0,
                 'question_id': sample.QUESTION_ID,
                 'is_accepted': False})

    def test_04_init_negative_score(self):

        with pytest.raises(answered.DiscardQuestion):
            _ = answered.Question(
                {'score': -3,
                 'question_id': sample.QUESTION_ID,
                 'is_accepted': False})

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

    def test_12_init_zero_score_accepted_answer(self):

        question = answered.Question({
            'score': 0,
            'question_id': 1,
            'is_accepted': True
        })

        assert question.user_score == 0
        assert question.useful is True
        assert question.inspect_answers is False
        assert question.views == 0
        assert question.answer_count == 0
        assert question.total_score == 0
        assert question.top_scores == []

    def test_13_init_negative_score_accepted_answer(self):

        question = answered.Question({
            'score': sample.NEGATIVE_SCORE,
            'question_id': sample.QUESTION_ID,
            'is_accepted': True
        })

        assert question.user_score == sample.NEGATIVE_SCORE
        assert question.useful is True
        assert question.inspect_answers is False
        assert question.views == 0
        assert question.answer_count == 0
        assert question.total_score == 0
        assert question.top_scores == []

    def test_14_update_no_view_count(self, regular_answered_question):
        with pytest.raises(ValueError,
                           match="Cannot retrieve view_count of the question"):
            regular_answered_question.update({})

    def test_15_update_str_view_count(self, regular_answered_question):
        with pytest.raises(ValueError,
                           match="Cannot retrieve view_count of the question"):
            regular_answered_question.update(
                {'view_count': "12K"})

    def test_16_update_no_answer_count(self, regular_answered_question):
        with pytest.raises(ValueError,
                           match="Cannot retrieve the number of answers for the question"):
            regular_answered_question.update(
                {'view_count': 42})

    def test_17_update_none_answer_count(self, regular_answered_question):
        with pytest.raises(ValueError,
                           match="Cannot retrieve the number of answers for the question"):
            regular_answered_question.update(
                {'view_count': 42,
                 'answer_count': None})

    def test_18_update_str_answer_count(self, regular_answered_question):
        with pytest.raises(ValueError,
                           match="Cannot retrieve the number of answers for the question"):
            regular_answered_question.update(
                {'view_count': 42,
                 'answer_count': "one"})

    def test_19_update_top_answer(self, regular_answered_question):
        views = 1024
        answer_count = answered.TOP_ANSWERS - 1

        regular_answered_question.update(
            {'view_count': views,
             'answer_count': answer_count})

        assert regular_answered_question.views == views
        assert regular_answered_question.answer_count == answer_count
        assert regular_answered_question.useful is True
        assert regular_answered_question.inspect_answers is False

    def test_20_update_many_answers(self, regular_answered_question):
        views = 1024
        answer_count = 12

        regular_answered_question.update(
            {'view_count': views,
             'answer_count': answer_count})

        assert regular_answered_question.views == views
        assert regular_answered_question.answer_count == answer_count
        assert regular_answered_question.useful is False
        assert regular_answered_question.inspect_answers is True

    def test_21_update_already_useful(self, accepted_answered_question):
        views = 1024
        answer_count = 12

        accepted_answered_question.update(
            {'view_count': views,
             'answer_count': answer_count})

        assert accepted_answered_question.views == views
        assert accepted_answered_question.answer_count == answer_count
        assert accepted_answered_question.useful is True
        assert accepted_answered_question.inspect_answers is False

    def test_22_inspect_dont_inspect_answers(self, answered_question_dont_inspect):

        low_score = answered.HALF_NICE - 1
        high_score = low_score + 10

        answered_question_dont_inspect.user_score = low_score
        answer = {'score': high_score}

        for _ in range(answered.TOP_ANSWERS):
            answered_question_dont_inspect.inspect_answer(answer)

        answered_question_dont_inspect.evaluate_answers()

        assert answered_question_dont_inspect.useful is True
        assert answered_question_dont_inspect.inspect_answers is False

    def test_23_inspect_all_scored_above(self, answered_question_require_inspection):

        low_score = answered.HALF_NICE - 1

        def roundup(number: float):
            return int(number) + bool(number % 1)

        # make it that other questions with higher score occupy all top answers above the user answer
        high_score = max(low_score + 1,
                         roundup(low_score * (1 / answered.SCORE_THRESHOLD - 1) / answered.TOP_ANSWERS))

        answered_question_require_inspection.user_score = low_score
        answered_question_require_inspection.inspect_answer({'score': low_score})

        for _ in range(answered.TOP_ANSWERS):
            answered_question_require_inspection.inspect_answer({'score': high_score})

        answered_question_require_inspection.evaluate_answers()

        assert answered_question_require_inspection.useful is False

    def test_24_inspect_equally_scored(self, answered_question_require_inspection):

        score = answered.HALF_NICE - 1

        answered_question_require_inspection.user_score = score

        for _ in range(answered.TOP_ANSWERS + 1):
            answered_question_require_inspection.inspect_answer({'score': score})

        answered_question_require_inspection.evaluate_answers()

        assert answered_question_require_inspection.useful is True

    def test_25_inspect_in_top(self, answered_question_require_inspection):

        user_score = answered.HALF_NICE - 1
        low_score = user_score - 1
        high_score = user_score / answered.SCORE_THRESHOLD

        answered_question_require_inspection.user_score = user_score

        answered_question_require_inspection.inspect_answer({'score': low_score})
        answered_question_require_inspection.inspect_answer({'score': user_score})

        for _ in range(answered.TOP_ANSWERS - 1):
            answered_question_require_inspection.inspect_answer({'score': high_score})

        answered_question_require_inspection.evaluate_answers()

        assert answered_question_require_inspection.useful is True
