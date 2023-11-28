import decimal
import os

import collections
import matplotlib.pyplot as plt
import numpy as np

from .ErrorAnalysisVO import ErrorAnalysisVO
from .StudentAnswerVO import StudentAnswerVO
from .config import set_matplotlib_params


class Student:
    output_path = os.path.join(".", "output_files")

    def __init__(self, name) -> None:
        self.name: str = name
        self.masked_name: str = self.__mask_name(self.name)
        self.answers: list[StudentAnswerVO] = []
        self.conditions = []
    
        self.score: decimal.Decimal = None

        self.error_analysis = collections.defaultdict(ErrorAnalysisVO)
        self.figure_path = None
        self.report = None

    def __mask_name(self, name):
        if len(name) <= 2:
            return name[0] + 'Ｏ' * (len(name) - 1)
        return f"{name[0]}{'Ｏ' * (len(name) - 2)}{name[-1]}"       

    def analyze_error(self):
        for error in self.error_analysis.values():
            error.calculate_percentage()

    def draw_figure(self):
        set_matplotlib_params()
        values = [err.percentage for err in self.error_analysis.values()]        
        angles = np.linspace(0, 2 * np.pi, len(values), endpoint=False) # 設置每個數據點的顯示位置，在雷達圖上用角度表示

        # 拼接數據首尾，使圖形中線條封閉
        values = np.concatenate((values,[values[0]]))
        angles = np.concatenate((angles,[angles[0]]))

        # 繪圖
        fig = plt.figure()
        ax = fig.add_subplot(111, polar=True)
        ax.plot(angles, values, 'o-', linewidth=2) # 繪製折線圖
        ax.fill(angles, values, alpha=0.25) # 填充顏色

        # 設置圖標上的角度劃分刻度，爲每個數據點處添加標籤
        ax.set_thetagrids(angles=(0,60,120,180,240,300), labels=self.error_analysis.keys(), fontsize=14)

        ax.set_ylim(0, 100) # 設置雷達圖的範圍
        ax.grid(True) # 添加網格線

        plt.savefig(os.path.join(self.output_path, 'static', self.name + ".png"))
        self.figure_path = os.path.join('.', 'static', self.name + ".png")
