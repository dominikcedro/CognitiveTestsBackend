"""
original author: Dominik Cedro
created: 2024-06-14
license: BSD 3.0
description: This module contains functions that calculate total score for given evaluation
"""


def calculate_total_score_stroop(mistake_count: int) -> int:
    max_mistakes = 20
    normalized_score = max(0, 100 - (mistake_count / max_mistakes) * 100)
    total_score_stroop = max(1, min(5, int(normalized_score // 20) + 1))
    return total_score_stroop

def calculate_total_score_trail_making(time: int, mistake_count: int) -> int:
    max_time = 300
    max_mistakes = 20
    time_score = max(0, 100 - (time / max_time) * 100)
    mistake_score = max(0, 100 - (mistake_count / max_mistakes) * 100)
    combined_score = (time_score + mistake_score) / 2
    total_score_trail = max(1, min(5, int(combined_score // 20) + 1))
    return total_score_trail

def calculate_total_score_digit_substitution(mistake_count: int, correct_answers: int) -> int:
    result = max(0, correct_answers - mistake_count)
    normalized_score = min(100, result * 5)  # Assuming 20 correct answers as max for a perfect score
    total_score_digit = max(1, min(5, int(normalized_score // 20) + 1))
    return total_score_digit
