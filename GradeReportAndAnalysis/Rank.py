import decimal
import random


class Rank:
    def __init__(self, students) -> None:
        self.students = students
        self.sorted_rank: dict = None
        self.pr88: decimal.Decimal
        self.pr75: decimal.Decimal
        self.pr50: decimal.Decimal
        self.pr25: decimal.Decimal

    def calculate_rank(self):
        sorted_students = self.students[:]
        sorted_students.sort(key=lambda x: x.score, reverse=True)
        ranks = [0] * len(sorted_students)

        cur_score, cur_rank, offset = sorted_students[0].score, 1, 0
        ranks[0] = cur_rank

        for idx, student in enumerate(sorted_students[1:], 1):
            if student.score == cur_score:
                ranks[idx] = cur_rank
                offset += 1
            else:
                cur_score = student.score
                cur_rank += 1
                ranks[idx] = cur_rank + offset
                cur_rank += offset
                offset = 0

        self.sorted_rank = {
            "students": [student for student, _ in zip(sorted_students, ranks)],
            "rank": [rank for _, rank in zip(sorted_students, ranks)],
        }

        self.__calculate_pr()

    def __find_onethird_bound(self, sorted_rank):
        """打亂並遮蔽第 1/3 名以下的成績"""
        n = len(self.students)
        bound = int(n / 3) - 1
        bound_rank = sorted_rank["rank"][bound]
        for idx, (_, cur_rk) in enumerate(
            zip(sorted_rank["students"], sorted_rank["rank"])
        ):
            next_rk = sorted_rank["rank"][idx + 1]
            if cur_rk == bound_rank and cur_rk != next_rk:
                bound = idx
                break
        return bound

    def random_rank(self):
        """打亂第 1/3 名以下的成績"""
        bound = self.__find_onethird_bound(self.sorted_rank)
        lower_stds = self.sorted_rank["students"][bound + 1 :]
        lower_rk = self.sorted_rank["rank"][bound + 1 :]
        lowers = []
        for std, rk in zip(lower_stds, lower_rk):
            lowers.append([std, rk])
        random.shuffle(lowers)
        lower_stds = [lower[0] for lower in lowers]
        lower_rk = [lower[1] for lower in lowers]
        self.sorted_rank = {
            "students": self.sorted_rank["students"][: bound + 1] + lower_stds,
            "rank": self.sorted_rank["rank"][: bound + 1] + lower_rk,
        }

    def hide_rank(self):
        """遮蔽 1/3 名以下的成績"""
        bound = self.__find_onethird_bound(self.sorted_rank)
        for idx in range(bound + 1, len(self.students)):
            self.sorted_rank["rank"][idx] = ""

    def __calculate_pr(self):
        """取得前標、均標等，排名採四捨五入"""
        n = len(self.students)

        self.pr88 = self.sorted_rank["students"][
            round(decimal.Decimal(str(n * (1 - 0.88)))) - 1
        ].score
        self.pr75 = self.sorted_rank["students"][
            round(decimal.Decimal(str(n * (1 - 0.75)))) - 1
        ].score
        self.pr50 = self.sorted_rank["students"][
            round(decimal.Decimal(str(n * (1 - 0.5)))) - 1
        ].score
        self.pr25 = self.sorted_rank["students"][
            round(decimal.Decimal(str(n * (1 - 0.25)))) - 1
        ].score
