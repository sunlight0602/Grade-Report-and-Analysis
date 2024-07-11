"""test Rank class"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.GradeReportAndAnalysis.rank import Rank


class TestRank(TestCase):
    """test Rank class"""

    @patch.object(Rank, "_calculate_pr")
    def test_calculate_rank(self, mock_calculate_pr):
        """test calculate_rank()"""
        student_1 = MagicMock(score=30)
        student_2 = MagicMock(score=10)
        student_3 = MagicMock(score=100)
        rank = Rank(students=[student_1, student_2, student_3])

        rank.calculate_rank()

        self.assertEqual(
            rank.sorted_rank,
            {"students": [student_3, student_1, student_2], "rank": [1, 2, 3]},
        )
        mock_calculate_pr.assert_called_once()
