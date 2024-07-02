from dataclasses import dataclass, field


@dataclass
class StudentAnswer:
    quest_num: int
    answer: str
    correction: str = field(init=False)
