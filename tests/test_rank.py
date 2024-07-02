import pytest

from GradeReportAndAnalysis.Rank import Rank
from GradeReportAndAnalysis.Student import Student


def set_students_scores(names, scores):
    ranks = []
    for student, score_ in zip(names, scores):
        std = Student(name=student)
        std.score = score_
        ranks.append(std)
    return ranks


@pytest.fixture
def test_case_1():
    names = ["沈小魚", "陳映羽", "陳冠廷", "歐冠女", "陳火昱婷", "屁孩一", "ASDFGASF"]
    scores = [100, 100, 46, 78, 100, 56, 48]
    ranks = set_students_scores(names, scores)
    ans = {
        "sorted_masked_names": [
            "沈Ｏ魚",
            "陳Ｏ羽",
            "陳ＯＯ婷",
            "歐Ｏ女",
            "屁Ｏ一",
            "AＯＯＯＯＯＯF",
            "陳Ｏ廷",
        ],
        "sorted_names": [
            "沈小魚",
            "陳映羽",
            "陳火昱婷",
            "歐冠女",
            "屁孩一",
            "ASDFGASF",
            "陳冠廷",
        ],
        "sorted_scores": [100, 100, 100, 78, 56, 48, 46],
        "sorted_ranks": [1, 1, 1, 4, 5, 6, 7],
        "sorted_hide_ranks": [1, 1, 1, "", "", "", ""],
        "pr88": 100,
        "pr75": 100,
        "pr50": 78,
        "pr25": 56,
    }
    return Rank(ranks), ans


@pytest.fixture
def test_case_2():
    names = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "任", "癸"]
    scores = [100, 100, 100, 100, 100, 100, 100, 100, 1, 100]
    ranks = set_students_scores(names, scores)
    ans = {
        "sorted_names": ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "癸", "任"],
        "sorted_scores": [100, 100, 100, 100, 100, 100, 100, 100, 100, 1],
        "sorted_ranks": [1, 1, 1, 1, 1, 1, 1, 1, 1, 10],
        "sorted_hide_ranks": [1, 1, 1, 1, 1, 1, 1, 1, 1, ""],
        "pr88": 100,
        "pr75": 100,
        "pr50": 100,
        "pr25": 100,
    }
    return Rank(ranks), ans


def test_calculate_rank(test_case_1, test_case_2):
    for test_case in [test_case_1, test_case_2]:
        rank, ans = test_case
        rank.calculate_rank()
        names, scores, ranks = [], [], []
        for std, rk in rank.sorted_rank:
            names.append(std.name)
            scores.append(std.score)
            ranks.append(rk)
        assert names == ans["sorted_names"], "Ranking error"
        assert scores == ans["sorted_scores"], "Ranking error"
        assert ranks == ans["sorted_ranks"], "Ranking error"


def test_random_rank(test_case_1):
    rank, ans = test_case_1
    rank.calculate_rank()
    rank.random_rank()
    names = [std.name for std, _ in rank.sorted_rank]
    assert names != ans["sorted_names"], "Ranking random error"


def test_hide_rank(test_case_1, test_case_2):
    for test_case in [test_case_1, test_case_2]:
        rank, ans = test_case
        rank.calculate_rank()
        rank.hide_rank()
        ranks = [rk for _, rk in rank.sorted_rank]
        assert ranks == ans["sorted_hide_ranks"], "Hide ranking error"


def test_pr(test_case_1, test_case_2):
    for test_case in [test_case_1, test_case_2]:
        rank, ans = test_case
        rank.calculate_rank()
        assert rank.pr88 == ans["pr88"], "Calculation error for pr88"
        assert rank.pr75 == ans["pr75"], "Calculation error for pr75"
        assert rank.pr50 == ans["pr50"], "Calculation error for pr50"
        assert rank.pr25 == ans["pr25"], "Calculation error for pr25"
