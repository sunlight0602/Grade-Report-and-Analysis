輸入：
./input_files/閱讀素養題目.xlsx
./input_files/學生劃卡狀況.xlsx
./input_files/學生閱讀素養答案.xlsx

輸出：
./output_files/static/[老師|學生名稱].png
./output_files/static/[老師|學生名稱].xlsx
./output_files/[老師|學生名稱].html

Reminder：                                                                                                                                                                                               
./output_files 裡面的 assets 提供了 bootstrap.css，務必下載
_windows 應該是最新的

Steps：
- venv
- install ../requirements.txt
- 把 draw_fig.py 和 main_windows.py 黏貼在一起到 .combine.py
- 在 windows 上執行 pyinstaller --onefile combine.py
- source ./script.sh
- ./dist 中的東西全部給客戶