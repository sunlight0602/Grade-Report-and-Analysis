import matplotlib.pyplot as plt

def set_matplotlib_params():
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'KaiTi', 'SimHei', 'FangSong', 'Arial Unicode MS'] # 用於正常顯示中文
    plt.rcParams['axes.unicode_minus'] = False # 用於正常顯示符號
    plt.style.use('ggplot') # 使用ggplot的繪圖風格，這個類似於美化了
