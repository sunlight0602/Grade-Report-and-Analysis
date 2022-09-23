from math import nan
import pandas as pd
import xlsxwriter
import matplotlib.pyplot as plt
import numpy as np

input_path = ".\\input_files\\"
speed = pd.read_excel(input_path + "作答速度.xlsx")

speed_dict = {}
for i in range(len(speed)):
    name = speed['學生'][i]
    speeds = []
    for j in range(1,6):
        temp = speed['作答速度'+str(j)][i]
        if not pd.isnull(temp):
            speeds.append(speed['作答速度'+str(j)][i])

    speed_dict[name] = speeds

print(speed_dict)