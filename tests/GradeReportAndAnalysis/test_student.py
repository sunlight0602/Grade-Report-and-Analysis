"""test Student class"""

import os
from decimal import Decimal
from unittest import TestCase

from src.GradeReportAndAnalysis.error_analysis import ErrorAnalysis
from src.GradeReportAndAnalysis.question import Question
from src.GradeReportAndAnalysis.student import Student
from src.GradeReportAndAnalysis.student_answer import StudentAnswer


class TestStudent(TestCase):
    """test Student class"""

    def test_initialize(self):
        """test initialize"""
        student = Student("沈小魚")

        self.assertEqual(student.name, "沈小魚")

    def test_mask_name(self):
        """test _mask_name()"""
        cases = [
            ("沈健康的魚", "沈ＯＯＯ魚"),
            ("沈健康魚", "沈ＯＯ魚"),
            ("沈小魚", "沈Ｏ魚"),
            ("沈魚", "沈Ｏ"),
            ("魚", "魚"),
        ]

        for name, expected in cases:
            with self.subTest((name, expected)):
                student = Student(name)

                self.assertEqual(student.masked_name, expected)

    def test_calculate_score(self):
        """test calculate_score()"""
        student = Student("沈小魚")
        for quest_num, s_ans in zip(
            range(1, 51),
            [
                "E",
                "E",
                "F",
                "F",
                "A",
                "A",
                "B",
                "B",
                "C",
                "A",
                "D",
                "B",
                "C",
                "D",
                "B",
                "A",
                "C",
                "C",
                "B",
                "C",
                "A",
                "A",
                "D",
                "C",
                "D",
                "B",
                "B",
                "B",
                "A",
                "A",
                "A",
                "B",
                "A",
                "C",
                "C",
                "C",
                "D",
                "D",
                "D",
                "C",
                "C",
                "C",
                "B",
                "C",
                "C",
                "B",
                "A",
                "D",
                "D",
                "B",
            ],
        ):
            student.answers.append(StudentAnswer(quest_num, s_ans))
        questions = [
            Question(1, "", "形音義", "D"),
            Question(2, "", "形音義", "B"),
            Question(3, "", "形音義", "C"),
            Question(4, "", "形音義", "C"),
            Question(5, "", "形音義", "A"),
            Question(6, "", "形音義", "D"),
            Question(7, "", "形音義", "B"),
            Question(8, "", "形音義", "D"),
            Question(9, "", "詞語使用", "D"),
            Question(10, "", "詞語使用", "A"),
            Question(11, "", "詞語使用", "D"),
            Question(12, "", "詞語使用", "B"),
            Question(13, "", "詞語使用", "C"),
            Question(14, "", "詞語使用", "B"),
            Question(15, "", "詞語使用", "B"),
            Question(16, "", "詞語使用", "A"),
            Question(17, "", "成語運用", "D"),
            Question(18, "", "成語運用", "C"),
            Question(19, "", "成語運用", "B"),
            Question(20, "", "成語運用", "C"),
            Question(21, "", "成語運用", "C"),
            Question(22, "", "成語運用", "A"),
            Question(23, "", "成語運用", "D"),
            Question(24, "", "成語運用", "C"),
            Question(25, "", "修辭技巧", "D"),
            Question(26, "", "修辭技巧", "B"),
            Question(27, "", "修辭技巧", "B"),
            Question(28, "", "修辭技巧", "B"),
            Question(29, "", "修辭技巧", "D"),
            Question(30, "", "修辭技巧", "A"),
            Question(31, "", "修辭技巧", "B"),
            Question(32, "", "修辭技巧", "C"),
            Question(33, "", "國學常識", "A"),
            Question(34, "", "國學常識", "C"),
            Question(35, "", "國學常識", "C"),
            Question(36, "", "國學常識", "B"),
            Question(37, "", "國學常識", "D"),
            Question(38, "", "國學常識", "D"),
            Question(39, "", "國學常識", "A"),
            Question(40, "", "國學常識", "B"),
            Question(41, "", "閱讀素養", "C"),
            Question(42, "", "閱讀素養", "B"),
            Question(43, "", "閱讀素養", "D"),
            Question(44, "", "閱讀素養", "A"),
            Question(45, "", "閱讀素養", "C"),
            Question(46, "", "閱讀素養", "B"),
            Question(47, "", "閱讀素養", "A"),
            Question(48, "", "閱讀素養", "C"),
            Question(49, "", "閱讀素養", "A"),
            Question(50, "", "閱讀素養", "D"),
        ]
        expected = {
            "name": "沈小魚",
            "error_analysis": {
                "形音義": ErrorAnalysis(correct=2, total=8),
                "詞語使用": ErrorAnalysis(correct=6, total=8),
                "成語運用": ErrorAnalysis(correct=6, total=8),
                "修辭技巧": ErrorAnalysis(correct=5, total=8),
                "國學常識": ErrorAnalysis(correct=5, total=8),
                "閱讀素養": ErrorAnalysis(correct=4, total=10),
            },
            "percentages": {
                "形音義": Decimal("25.0"),
                "詞語使用": Decimal("75.0"),
                "成語運用": Decimal("75.0"),
                "修辭技巧": Decimal("62.5"),
                "國學常識": Decimal("62.5"),
                "閱讀素養": Decimal("40.0"),
            },
            "labels": student.error_analysis.keys(),
            "score": 56,
        }

        student.calculate_score(questions)

        for label, err in student.error_analysis.items():
            self.assertEqual(err.percentage, expected["percentages"][label])
            self.assertEqual(err.correct, expected["error_analysis"][label].correct)
            self.assertEqual(err.total, expected["error_analysis"][label].total)

        student.get_figure()
        self.assertEqual(student.figure.name, expected["name"])
        self.assertEqual(student.figure.values, list(expected["percentages"].values()))
        self.assertEqual(student.figure.labels, expected["labels"])
        self.assertEqual(
            student.figure.path,
            os.path.join(
                os.getcwd(), "output_files", "static", f'{expected["name"]}.png'
            ),
        )

        self.assertEqual(student.score, expected["score"])
