import os

import matplotlib.pyplot as plt
import numpy as np

from .config import set_matplotlib_params


class Figure:
    output_path = os.path.join(os.getcwd(), 'output_files')

    def __init__(self, name, values, labels) -> None:
        self.name: str = name
        self.values = values
        self.labels = labels
        self.path: str
        
        self.draw_figure()

    def draw_figure(self):
        set_matplotlib_params()

        values = self.values
        angles = np.linspace(0, 2 * np.pi, len(values), endpoint=False) # 設置每個數據點的顯示位置，在雷達圖上用角度表示

        # 拼接數據首尾，使圖形中線條封閉
        values = np.concatenate((values, [values[0]]))
        angles = np.concatenate((angles, [angles[0]]))

        # 繪圖
        fig = plt.figure()
        ax = fig.add_subplot(111, polar=True)
        ax.plot(angles, values, 'o-', linewidth=2) # 繪製折線圖
        ax.fill(angles, values, alpha=0.25) # 填充顏色

        # 設置圖標上的角度劃分刻度，爲每個數據點處添加標籤
        ax.set_thetagrids(angles=(0,60,120,180,240,300), labels=self.labels, fontsize=14)

        ax.set_ylim(0, 100) # 設置雷達圖的範圍
        ax.grid(True) # 添加網格線

        plt.savefig(os.path.join(self.output_path, 'static', f'{self.name}.png'))
        self.path = os.path.join(os.getcwd(), 'static', f'{self.name}.png')
