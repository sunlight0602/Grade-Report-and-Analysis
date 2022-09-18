import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set matplotlib parameters
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'KaiTi', 'SimHei', 'FangSong', 'Arial Unicode MS'] # 用於正常顯示中文
plt.rcParams['axes.unicode_minus'] = False # 用於正常顯示符號
plt.style.use('ggplot') # 使用ggplot的繪圖風格，這個類似於美化了

# File path:
output_path = './output_files/'
input_path = "./input_files/"

def draw_fig(student_name, class_dict, student_dict):
    """
    student_name (str): name of the student
    class_dict (dict): class: amount of questions in the class
    student_dict (dict): class: amount of questions in the class, which is written correctly
    """
    values = []
    for class_ in class_dict.keys():
        values.append(student_dict[class_] / class_dict[class_] * 100)
    
    angles = np.linspace(0, 2*np.pi, len(values), endpoint=False) # 設置每個數據點的顯示位置，在雷達圖上用角度表示

    # 拼接數據首尾，使圖形中線條封閉
    values = np.concatenate((values,[values[0]]))
    angles = np.concatenate((angles,[angles[0]]))

    # 繪圖
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, values, 'o-', linewidth=2) # 繪製折線圖
    ax.fill(angles, values, alpha=0.25) # 填充顏色

    # 設置圖標上的角度劃分刻度，爲每個數據點處添加標籤
    ax.set_thetagrids(angles=(0,60,120,180,240,300), labels=class_dict.keys(), fontsize=14)

    ax.set_ylim(0, 100) # 設置雷達圖的範圍
    # plt.title(student_name + "的考卷分析") # 添加標題
    ax.grid(True) # 添加網格線

    plt.savefig(output_path + student_name + ".png")

    return

def draw_teacher_fig(wrong_dict, num_of_student, class_dict):
    values = []
    for class_, amount in wrong_dict.items():
        values.append(round((class_dict[class_]*num_of_student - amount) / num_of_student / class_dict[class_] * 100, 2))

    # print(values)
    angles = np.linspace(0, 2*np.pi, len(values), endpoint=False) # 設置每個數據點的顯示位置，在雷達圖上用角度表示

    # 拼接數據首尾，使圖形中線條封閉
    values = np.concatenate((values,[values[0]]))
    angles = np.concatenate((angles,[angles[0]]))

    # 繪圖
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, values, 'o-', linewidth=2) # 繪製折線圖
    ax.fill(angles, values, alpha=0.25) # 填充顏色

    # 設置圖標上的角度劃分刻度，爲每個數據點處添加標籤
    ax.set_thetagrids(angles=(0,60,120,180,240,300), labels=wrong_dict.keys(), fontsize=14)

    ax.set_ylim(0, 100) # 設置雷達圖的範圍
    ax.grid(True) # 添加網格線

    plt.savefig(output_path + "給老師看的.png")