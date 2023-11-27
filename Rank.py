import decimal
import random

class Rank:
    def __init__(self, students) -> None:
        self.students = students
        self.sorted_rank: list = None
        self.pr88: decimal.Decimal
        self.pr75: decimal.Decimal
        self.pr50: decimal.Decimal
        self.pr25: decimal.Decimal
    
    def calculate_rank(self, masked=False, random=False):
        scores = [[student.masked_name if masked else student.name, student.score] for student in self.students]
        scores.sort(key=lambda x: x[1], reverse=True)

        cur_score, cur_rank, offset = scores[0][0], 1, 0

        scores[0].append(cur_rank)

        for idx, (score, _) in enumerate(scores[1:], 1):
            if score == cur_score:
                scores[idx].append(cur_rank)
                offset += 1
            else:
                cur_score = score
                cur_rank += 1
                scores[idx].append(cur_rank + offset)
                cur_rank += offset
                offset = 0
        self.sorted_rank = scores
        self.__calculate_pr()

        if random:
            self.__random_rank(scores)

    def __random_rank(self, sorted_rank, masked=True):
        """打亂第 1/3 名以下的成績"""
        n = len(sorted_rank)
        bound = int(n / 3) - 1
        bound_rank = sorted_rank[bound][2]
        for idx, (_, _, cur_rk) in enumerate(sorted_rank):
            next_rk = sorted_rank[idx + 1][2]
            if cur_rk == bound_rank and cur_rk != next_rk:
                bound = idx
                break
        lowers = sorted_rank[bound + 1:]
        random.shuffle(lowers)
        if masked:
            for idx in range(len(lowers)):
                lowers[idx][2] = ''
        self.sorted_rank = sorted_rank[:bound + 1] + lowers

    def __calculate_pr(self):
        """取得前標、均標等"""
        n = len(self.students)
        self.pr88 = self.sorted_rank[round(n * (1 - 0.88)) - 1][1]
        self.pr75 = self.sorted_rank[round(n * (1 - 0.75)) - 1][1]
        self.pr50 = self.sorted_rank[round(n * (1 - 0.5)) - 1][1]
        self.pr25 = self.sorted_rank[round(n * (1 - 0.25)) - 1][1]
