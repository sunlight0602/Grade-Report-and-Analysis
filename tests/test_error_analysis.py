"""tests for ErrorAnalysis class"""

from decimal import Decimal
from unittest import TestCase

from GradeReportAndAnalysis.error_analysis import ErrorAnalysis


class TestErrorAnalysis(TestCase):
    """test ErrorAnalysis class"""

    def test_initialize(self):
        """test initialize"""
        error_analysis = ErrorAnalysis(correct=3, total=5)

        self.assertEqual(error_analysis.correct, 3)
        self.assertEqual(error_analysis.total, 5)
        self.assertNotIn("percentage", vars(error_analysis))

    def test_calculate_percentage(self):
        """test calculate_percentage()"""
        scores = [
            (3, 5, "60"),
            (11, 50, "22"),
            (13, 50, "26"),
            (15, 50, "30"),
            (2, 4, "50"),
            (20, 100, "20"),
            (3.15, 100, "3.2"),
        ]

        for correct, total, expect in scores:
            with self.subTest((correct, total, expect)):
                error_analysis = ErrorAnalysis(correct=correct, total=total)

                error_analysis.calculate_percentage()

                self.assertEqual(error_analysis.percentage, Decimal(expect))
