"""
original author: Dominik Cedro
created: 2024-06-14
license: BSD 3.0
description: This module contains functions that calculate total score for given evaluation
"""


def calculate_total_score_stroop(mistake_count: int) -> int:
    num_questions = 20
    if mistake_count <= num_questions * 0.1:
        total_score_stroop = 5
    elif mistake_count <= num_questions * 0.2:
        total_score_stroop = 4
    elif mistake_count <= num_questions * 0.4:
        total_score_stroop = 3
    elif mistake_count <= num_questions * 0.6:
        total_score_stroop = 2
    else:
        total_score_stroop = 1
    return total_score_stroop


def calculate_total_score_trail_making(time: int, mistake_count: int) -> int:
    base_score = 6
    total_score_trail = max(1, min(5, int(base_score - (time / 300 + mistake_count / 30) * 2.5)))
    return total_score_trail


def calculate_total_score_digit_substitution(mistake_count: int, correct_answers: int, total_time: int = 120) -> int:
    total_attempts = mistake_count + correct_answers
    if total_attempts == 0 or total_time == 0:
        return 1
    accuracy = correct_answers / total_attempts
    time_efficiency = correct_answers / total_time
    total_score_digit = max(1, min(5, int(1 + 2 * accuracy + 2 * time_efficiency)))
    return total_score_digit
