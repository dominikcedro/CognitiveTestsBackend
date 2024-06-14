"""
original author: Dominik Cedro
created: 2024-06-14
license: BSD 3.0
description: This module contains functions that calculate total score for given evaluation
"""


def calculate_total_score_stroop(mistake_count:int):
    # mozna miec maks 20 bledow
    CEILING_POINTS: int = 100
    total_score_stroop = 100 - (5 * mistake_count)
    if total_score_stroop < 0:
        total_score_stroop = 0
    return total_score_stroop

def calculate_total_score_trail_making(time:int, mistake_count:int):
    # max moze byc

    pass

def calculate_total_score_digit_substitution(mistake_count:int, correct_answers: int):
    result = correct_answers - mistake_count
    # czas to dwie minuty i tyle ile naklikasz tyle wejdzie
    # są błędy
    pass