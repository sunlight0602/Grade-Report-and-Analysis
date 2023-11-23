import decimal

class Rank:
    def __init__(self, students) -> None:
        self.students = students
        self.sorted_rank: list = self.calculate_rank(masked=False, random=False)
        self.__calculate_pr()
        self.pr88: decimal.Decimal
        self.pr75: decimal.Decimal
        self.pr50: decimal.Decimal
        self.pr25: decimal.Decimal
    
    def calculate_rank(self, masked=False, random=False):
        if masked:
            scores = [[student.masked_name, student.score] for student in self.students]    
        else:
            scores = [[student.name, student.score] for student in self.students]
        scores.sort(key=lambda x: x[1], reverse=True)

        cur_score, cur_rank = scores[0][0], 1
        offset = 0

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
        return scores
    
    def __calculate_pr(self):
        # 取得前標均標等
        n = len(self.students)
        self.pr88 = self.sorted_rank[round(n * (1 - 0.88)) - 1][1]
        self.pr75 = self.sorted_rank[round(n * (1 - 0.75)) - 1][1]
        self.pr50 = self.sorted_rank[round(n * (1 - 0.5)) - 1][1]
        self.pr25 = self.sorted_rank[round(n * (1 - 0.25)) - 1][1]
