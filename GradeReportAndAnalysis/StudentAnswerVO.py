from dataclasses import dataclass, field

@dataclass
class StudentAnswerVO:
    quest_num: int
    answer: str
    correction: str = field(init=False)