from impact.answered import Question


def question(**kwargs) -> Question:
    result = Question(kwargs)

    for key, value in kwargs.items():
        if hasattr(result, key):
            result.__setattr__(key, value)

    return result


ASKED_QUESTIONS_10_1000 = {question_id: 1000 for question_id in range(1, 11)}

ANSWERED_QUESTIONS_10_1000_ALL_USEFUL = {
    question_id: question(
        question_id=question_id,
        views=1000,
        is_accepted=False,
        score=1,
        useful=True) for question_id in range(1, 11)
}

ANSWERED_QUESTIONS_10_1000_ALL_USELESS = {
    question_id: question(
        question_id=question_id,
        views=1000,
        is_accepted=False,
        score=1,
        useful=False) for question_id in range(1, 11)
}

ANSWERED_QUESTIONS_20_1000_HALF_USEFUL = {
    question_id: question(
        question_id=question_id,
        views=1000,
        is_accepted=False,
        score=1,
        useful=question_id > 10) for question_id in range(1, 21)
}

USER_ID = 1
QUESTION_ID = 13000
ANSWER_ID = 99000
NICE_QUESTION_SCORE = 10
NEGATIVE_SCORE = -4
