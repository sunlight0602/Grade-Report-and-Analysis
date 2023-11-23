
from dataclasses import dataclass

@dataclass
class QuestionVO:
    """Class that contains basic information about a question."""

    quest_num: int
    description: str
    category: str
    answer: str
    