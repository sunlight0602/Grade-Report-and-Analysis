from dataclasses import dataclass


@dataclass
class Question:
    """Class that contains basic information about a question."""

    quest_num: int
    description: str
    category: str
    answer: str
