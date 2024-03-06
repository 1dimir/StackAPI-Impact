import tests.data as sample
import stackapi_impact as impact
from tests.fixtures import impact_no_api


class TestEvaluateAnswers:

    def test_01_no_questions(self, impact_no_api: impact.StackExchangeImpact):

        impact_no_api._evaluate_answers()

        assert len(impact_no_api._answered_questions) == 0

    def test_02_extra_questions(self, impact_no_api: impact.StackExchangeImpact):

        impact_no_api._answered_questions[sample.QUESTION_ID] = sample.question(
            inspect_answers=True,
            question_id=sample.QUESTION_ID,
            score=1,
            top_scores=[1, 2, 3],
            total_score=100,
            is_accepted=False)

        impact_no_api._evaluate_answers([sample.QUESTION_ID + 1])  # different id

        assert len(impact_no_api._answered_questions) == 1
        assert sample.QUESTION_ID + 1 not in impact_no_api._answered_questions
        assert impact_no_api._answered_questions[sample.QUESTION_ID].useful is False

    def test_03_process_inspect_answers(self, impact_no_api: impact.StackExchangeImpact):

        impact_no_api._answered_questions[sample.QUESTION_ID] = sample.question(
            inspect_answers=True,
            question_id=sample.QUESTION_ID,
            score=1,
            top_scores=[1, 2, 3],
            total_score=100,
            is_accepted=False)

        impact_no_api._evaluate_answers()

        assert len(impact_no_api._answered_questions) == 1
        assert impact_no_api._answered_questions[sample.QUESTION_ID].useful is True

    def test_04_hit_top_scores(self, impact_no_api: impact.StackExchangeImpact):

        impact_no_api._answered_questions[sample.QUESTION_ID] = sample.question(
            inspect_answers=True,
            question_id=sample.QUESTION_ID,
            score=1,
            top_scores=[1, 2, 3],
            total_score=100,
            is_accepted=False)

        impact_no_api._evaluate_answers([sample.QUESTION_ID])

        assert len(impact_no_api._answered_questions) == 1
        assert impact_no_api._answered_questions[sample.QUESTION_ID].useful is True

    def test_05_hit_score_threshold(self, impact_no_api: impact.StackExchangeImpact):

        impact_no_api._answered_questions[sample.QUESTION_ID] = sample.question(
            inspect_answers=True,
            question_id=sample.QUESTION_ID,
            score=4,
            top_scores=[5, 5, 5],
            total_score=19,
            is_accepted=False)

        impact_no_api._evaluate_answers([sample.QUESTION_ID])

        assert len(impact_no_api._answered_questions) == 1
        assert impact_no_api._answered_questions[sample.QUESTION_ID].useful is True
