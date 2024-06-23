"""
original author: Dominik Cedro
created: 2024-06-14
license: BSD 3.0
description: This module contains functions that calculate total score for given evaluation
"""

import math


def calculate_total_score_stroop(mistake_count: int) -> int:
    total_score_stroop = max(1, min(5, 6 - int((mistake_count / 30) * 5)))
    return total_score_stroop

def calculate_total_score_trail_making(time: int, mistake_count: int) -> int:
    base_score = 6
    total_score_trail = max(1, min(5, int(base_score - (time / 300 + mistake_count / 30) * 2.5)))
    return total_score_trail

def calculate_total_score_digit_substitution(mistake_count: int, correct_answers: int) -> int:
    total_attempts = mistake_count + correct_answers
    if total_attempts == 0:
        return 1
    accuracy = correct_answers / total_attempts
    total_score_digit = max(1, min(5, int(1 + 4 * accuracy)))
    return total_score_digit
