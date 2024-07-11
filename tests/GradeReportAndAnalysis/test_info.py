"""test info class"""

import os
from unittest import TestCase

from src.GradeReportAndAnalysis.info import Info


class TestInfo(TestCase):
    """test Info class"""

    # @patch.object(Info, "_read_excel")
    # def test_initialize(self, mock_read_excel):
    def test_initialize(self):
        """test initialize"""
        info = Info(file_name="./1214_第２次全民中檢模擬考.xlsx")

        self.assertEqual(info.title, "第２次全民中檢模擬考")
        self.assertEqual(info.level, "中等")
        self.assertEqual(info.date, "2023/12/14")
        # self.assertIsNone(info.title)

    def test_read_excel(self):
        """test _read_excel()"""
        input_path = os.path.join(
            os.getcwd(), "input_files", "1214_第２次全民中檢模擬考.xlsx"
        )
        info = Info(file_name=input_path)
        ans = {
            "title": "第２次全民中檢模擬考",
            "level": "中等",
            "date": "2023/12/14",
            "question_numbers": [i for i in range(1, 51)],
            "descriptions": [
                "下列文句中「」的字，何者讀音正確？ A「蝙」蝠──「ㄅㄧㄢˇ」 B 神采「熠熠」──「ㄓㄜˊ」 C「興」奮──「ㄒㄧㄥˋ」 D 一語成「讖」──「ㄔㄣˋ」"
            ]
            + [""] * 49,
            "categories": ["形音義"] * 8
            + ["詞語使用"] * 8
            + ["成語運用"] * 8
            + ["修辭技巧"] * 8
            + ["國學常識"] * 8
            + ["閱讀素養"] * 10,
            "answers": [
                "D",
                "B",
                "C",
                "C",
                "A",
                "D",
                "B",
                "D",
                "D",
                "A",
                "D",
                "B",
                "C",
                "B",
                "B",
                "A",
                "D",
                "C",
                "B",
                "C",
                "C",
                "A",
                "D",
                "C",
                "D",
                "B",
                "B",
                "B",
                "D",
                "A",
                "B",
                "C",
                "A",
                "C",
                "C",
                "B",
                "D",
                "D",
                "A",
                "B",
                "C",
                "B",
                "D",
                "A",
                "C",
                "B",
                "A",
                "C",
                "A",
                "D",
            ],
            "names": [
                "沈小魚",
                "陳映羽",
                "陳冠廷",
                "歐冠女",
                "陳火昱婷",
                "屁孩一",
                "ASDFGASF",
            ],
            "std1_answers": [
                "D",
                "B",
                "C",
                "C",
                "A",
                "D",
                "B",
                "D",
                "D",
                "A",
                "D",
                "B",
                "C",
                "B",
                "B",
                "A",
                "D",
                "C",
                "B",
                "C",
                "C",
                "A",
                "D",
                "C",
                "D",
                "B",
                "B",
                "B",
                "D",
                "A",
                "B",
                "C",
                "A",
                "C",
                "C",
                "B",
                "D",
                "D",
                "A",
                "B",
                "C",
                "B",
                "D",
                "A",
                "C",
                "B",
                "A",
                "C",
                "A",
                "D",
            ],
            "std1_conditions": ["顏色太深"],
        }

        for idx, question in enumerate(info.questions):
            self.assertEqual(question.quest_num, ans["question_numbers"][idx])
            self.assertEqual(question.description, ans["descriptions"][idx])
            self.assertEqual(question.category, ans["categories"][idx])
            self.assertEqual(question.answer, ans["answers"][idx])

        for idx, student in enumerate(info.students):
            self.assertEqual(student.name, ans["names"][idx])

        for i, answer in enumerate(info.students[0].answers):
            self.assertEqual(student.name, ans["names"][idx])

        for i, cond in enumerate(info.students[0].conditions):
            self.assertEqual(cond, ans["std1_conditions"][i])
