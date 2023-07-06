import pandas as pd
import xlsxwriter
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# File path:
output_path = os.path.join(".", "output_files")
input_path = os.path.join(".", "input_files")
static_path = os.path.join(output_path, "static")

# ======= for figure ======

# Set matplotlib parameters
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'KaiTi', 'SimHei', 'FangSong', 'Arial Unicode MS'] # 用於正常顯示中文
plt.rcParams['axes.unicode_minus'] = False # 用於正常顯示符號
plt.style.use('ggplot') # 使用ggplot的繪圖風格，這個類似於美化了

def draw_student_fig(student_name, class_dict, student_dict):
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

    plt.savefig(os.path.join(static_path, student_name+".png"))

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

    # plt.savefig(output_path + "給老師看的.png")
    plt.savefig(os.path.join(static_path, "給老師看的.png"))

# ===== main =====

# Read files
exam_paper = pd.read_excel(os.path.join(input_path, "閱讀素養題目.xlsx"))
student_answer = pd.read_excel(os.path.join(input_path, "學生閱讀素養答案.xlsx"), converters={'學生/題號': int})
# writing_score = pd.read_excel(input_path + "寫作測驗分數.xlsx")
bubbles = pd.read_excel(os.path.join(input_path, "學生劃卡狀況.xlsx"))
writing_score_dict = {}
bubbles_dict = {}
# for idx in range(len(writing_score)):
#     writing_score_dict[writing_score.iloc[idx]["學生"]] = writing_score.iloc[idx]["寫作分數"]
for idx in range(len(bubbles)):
    bubbles_dict[bubbles.iloc[idx]["學生"]] = []
    bubbles_dict[bubbles.iloc[idx]["學生"]].append(bubbles.iloc[idx]["劃卡狀況1"])
    bubbles_dict[bubbles.iloc[idx]["學生"]].append(bubbles.iloc[idx]["劃卡狀況2"])
    bubbles_dict[bubbles.iloc[idx]["學生"]].append(bubbles.iloc[idx]["劃卡狀況3"])
    bubbles_dict[bubbles.iloc[idx]["學生"]].append(bubbles.iloc[idx]["劃卡狀況4"])
    bubbles_dict[bubbles.iloc[idx]["學生"]].append(bubbles.iloc[idx]["劃卡狀況5"])
    bubbles_dict[bubbles.iloc[idx]["學生"]].append(bubbles.iloc[idx]["劃卡狀況6"])

# Determine amount of questions and students
num_of_question, num_of_student = student_answer.shape
num_of_student -= 1

# Read from exam_paper
questions = list(exam_paper['題號']) # Question numbers
answers = list(exam_paper['解答']) # Correct answers
classes = list(exam_paper['單元名稱']) # Question class

# Initialize dictionaries
class_dict = {}
student_dict = {}
wrong_dict = {}
for class_ in classes:
    if class_ in class_dict:
        class_dict[class_] += 1 # Class: amount of questions
    else:
        class_dict[class_] = 1
        # student_dict[class_] = 0 # Class: 0
        wrong_dict[class_] = 0 # Class: amount of mistakes

question_dict = {}
for question in questions:
    if question not in question_dict:
        question_dict[question] = 0 # 題號: 0

# 準備個人分析圖的 headers
headers = ["題號", "單元名稱", "答題狀況"]
for class_ in class_dict.keys():
    headers.append(class_) # ["題號", "單元名稱", "答題狀況", "文字", "修辭"...]

# print(student_answer)
# print(student_answer["黃子恩"][49])
# print(class_dict)

assert student_answer.shape[0] == len(answers)

student_score = []
for i in range(num_of_student):
    student_name = student_answer.columns[i+1]
    print('學生名稱:', student_name)

    workbook = xlsxwriter.Workbook(os.path.join(static_path, student_name+".xlsx"))
    worksheet = workbook.add_worksheet()

    for idx, header in enumerate(headers):
        worksheet.write(0, idx, header)
    
    # for class_ in student_dict.keys():
    #     student_dict[class_] = 0
    student_dict[student_name] = {}
    for class_ in class_dict.keys():
        student_dict[student_name][class_] = 0

    correct = 0
    row = 1
    for question, answer, class_ in zip(questions, answers, classes): # 題號 正確解答 題目類別
        # print(question, answer, class_)
        worksheet.write(row, 0, question) # 題號
        worksheet.write(row, 1, class_) # 題目類別
        if student_answer[student_name][question-1] == answer:
            worksheet.write(row, 2, "O")
            correct += 1
            student_dict[student_name][class_] += 1
        else:
            worksheet.write(row, 2, "X")
            question_dict[question] += 1
            wrong_dict[class_] += 1
        row += 1
        
    for idx, class_  in enumerate(class_dict.keys()):
        worksheet.write(1, 3+idx, str(student_dict[student_name][class_]) + '/' + str(class_dict[class_]))
    
    print('分數:', int(correct / num_of_question * 100))
    workbook.close()

    student_score.append((student_name, int(correct / num_of_question * 100)))

    # =====

    print(student_dict[student_name])
    draw_student_fig(student_name, class_dict, student_dict[student_name])

# ====

workbook = xlsxwriter.Workbook(os.path.join(static_path, '給老師看的.xlsx'))
worksheet = workbook.add_worksheet()
worksheet.write(0, 0, "題號")
worksheet.write(0, 1, "單元名稱")
worksheet.write(0, 2, "答錯人數")
worksheet.write(0, 3, "答錯比例")
worksheet.write(0, 5, "人數")
worksheet.write(0, 6, "分數")
worksheet.write(0, 7, "總題數")
worksheet.write(1, 7, str(num_of_question))
worksheet.write(0, 8, "總分")
worksheet.write(1, 8, "100")

# print(wrong_dict)

for idx, (class_, amount) in enumerate(class_dict.items()):
    worksheet.write(0, idx+9, class_)
    worksheet.write(1, idx+9, amount)
    worksheet.write(2, idx+9, str(round(wrong_dict[class_] / num_of_student, 2))+" 題／人")
draw_teacher_fig(wrong_dict, num_of_student, class_dict)

student_score.sort(key=lambda x: x[1], reverse=True)
# print(student_score)
# print(sum([s for _, s in student_score[:int(len(student_score)*0.5)]]))

worksheet.write(1, 4, "本梯次成績前２％分數")
if int(len(student_score)*0.02) == 0:
    worksheet.write(1, 6, student_score[0][1])
    worksheet.write(1, 5, "1")
else:
    worksheet.write(1, 6, sum([s for _, s in student_score[:int(len(student_score)*0.02)]]) / int(len(student_score)*0.02))
    worksheet.write(1, 5, int(len(student_score)*0.02))


worksheet.write(2, 4, "高標（成績前５０％平均分數）")
worksheet.write(2, 6, sum([s for _, s in student_score[:int(len(student_score)*0.5)]]) / int(len(student_score)*0.5))
worksheet.write(2, 5, int(len(student_score)*0.5))

worksheet.write(3, 4, "均標（成績平均分數）")
worksheet.write(3, 6, round(sum([s for _, s in student_score]) / len(student_score),2) )
worksheet.write(3, 5, len(student_score))

worksheet.write(4, 4, "低標（成績後５０％平均分數）")
worksheet.write(4, 6, sum([s for _, s in student_score[int(len(student_score)*0.5):]]) / int(len(student_score)*0.5))
worksheet.write(4, 5, int(len(student_score)*0.5))

row = 1
for class_, (question, wrong_num) in zip(classes, question_dict.items()):
    worksheet.write(row, 0, question)
    worksheet.write(row, 1, class_)
    worksheet.write(row, 2, str(wrong_num) + '/' + str(num_of_student))
    worksheet.write(row, 3, str(int(wrong_num / num_of_student * 100)) + "%")
    row += 1


workbook.close()

# ======= Make student HTML =======

def ranking(student_score):
    student_score.sort(key=lambda x: x[1], reverse=True)
    cur_score = student_score[0][1] # score of first place
    student_score[0] = student_score[0] + (1,)
    cur_rank = 1
    offset = 0

    for idx, ss in enumerate(student_score[1:]):
        if ss[1] == cur_score:
            ss = ss + (cur_rank,)
            offset += 1
        else:
            cur_rank = cur_rank + 1
            ss = ss + (cur_rank + offset,)
        student_score[idx+1] = ss
    return student_score

student_score = ranking(student_score)
# print(student_score)

# Get first three places:
# first_place = student_score[0][1]
# second_place = 0
# for _, score in student_score[1:]:
#     second_place = score
#     if second_place != first_place:
#         break
# third_place = 0
# for _, score in student_score[1:]:
#     third_place = score
#     if third_place != second_place != first_place:
#         break

# 打亂第四名以下的成績
import random
import math
one_third_idx = math.ceil(num_of_student / 3) - 1
one_third_rank = student_score[one_third_idx][2]
for idx, (name, score, rank) in enumerate(student_score):
    if rank == one_third_rank and student_score[idx+1][2] != one_third_rank:
        one_third_idx = idx
        break
student_behind = student_score[one_third_idx+1:]
random.shuffle(student_behind)
student_score = student_score[:one_third_idx+1] + student_behind
print(student_score)

time = exam_paper["第幾次"][0]  # 第 1 次全民中檢仿真模擬考
level = exam_paper["級別"][0]  # 級別：初等
date = exam_paper["測驗日期"][0]  # 級別：初等
for student, score, rank in student_score:
    file = open(os.path.join(output_path, student+".html"), "w", encoding='utf-8')

    file.write('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>煜婷國文</title><link rel="stylesheet" href="./assets/css/bootstrap.min.css"></head><body><div class="container"><div class="row">')
    file.write('<div class="col-8" style="padding-left: 0px !important">')
    file.write('<p class="h2"><strong>煜婷國文<br>第' + time + '次全民中檢仿真模擬考</strong></p>')
    file.write('</div><div class="col-4 text-right" style="padding-right: 0px !important">')
    file.write('<p class="h6">測驗日期：' + date.strftime("%Y/%m/%d") + '</p>')
    file.write('<p class="h6">檢定級別：' + level + '</p>')
    file.write('</div></div><div class="row"><p class="h5"><strong>總體成績概要：</strong></p><table class="table text-center table-bordered table-sm"><thead><tr class="table-secondary"><th>姓名</th><th>語文素養</th><th>檢定結果</th><th>畫卡狀況</th></tr></thead><tbody><tr>')
    file.write('<td class="align-middle">' + student + '</td>')
    file.write('<td class="align-middle">' + str(score) + '</td>')
    # file.write('<td class="align-middle">' + str(writing_score_dict[student]) + '</td>')
    if score >= 66:
        file.write('<td class="align-middle">語文素養 ☑ 通過 ☐ 未通過<br>')
    else:
        file.write('<td class="align-middle">語文素養 ☐ 通過 ☑ 未通過<br>')
    # if writing_score_dict[student] == "本次未考":
    #     file.write('寫作測驗 ☑ 本次未考</td>')
    # elif writing_score_dict[student] >= 4:
    #     file.write('寫作測驗 ☑ 通過 ☐ 未通過</td>')
    # else:
    #     file.write('寫作測驗 ☐ 通過 ☑ 未通過</td>')
    file.write('<td class="align-middle"><div class="row align-middle"><div class="col align-middle">')

    if "正確標準" in bubbles_dict[student]:
        file.write('☑ 正確標準<br>')
    else:
        file.write('☐ 正確標準<br>')
    if "顏色太深" in bubbles_dict[student]:
        file.write('☑ 顏色太深<br>')
    else:
        file.write('☐ 顏色太深<br>')
    if "顏色太淺" in bubbles_dict[student]:
        file.write('☑ 顏色太淺')
    else:
        file.write('☐ 顏色太淺')

    file.write('</div><div class="col align-middle">')

    if "凸出格外" in bubbles_dict[student]:
        file.write('☑ 凸出格外<br>')
    else:
        file.write('☐ 凸出格外<br>')
    if "未塗滿格" in bubbles_dict[student]:
        file.write('☑ 未塗滿格<br>')
    else:
        file.write('☐ 未塗滿格<br>')
    if "擦拭不淨" in bubbles_dict[student]:
        file.write('☑ 擦拭不淨')
    else:
        file.write('☐ 擦拭不淨')

    file.write('</div></row></td></tr></tbody></table><p>檢定通過標準：語文素養達 66 分以上</p></div><div class="row"><p class="h5"><strong>語文素養答題狀況：</strong></p><table class="table table-bordered text-center table-sm"><tbody><tr class="table-secondary">')
    for i in range(1,26): # 題號
        file.write('<td>' + str(i) +'</td>')
    file.write('</tr><tr>') 
    for answer in answers[:25]: # 正解
        file.write('<td>' + answer +'</td>')
    file.write('</tr><tr>')
    for i in range(0,25): # 學生作答
        if student_answer[student][i] == answers[i]:
            file.write('<td>.</td>')
        else:
            file.write('<td>' + student_answer[student][i] + '</td>')
    file.write('</tr>')

    file.write('<tr class="table-secondary">')
    for i in range(26,51): # 題號
        file.write('<td>' + str(i) +'</td>')
    file.write('</tr><tr>')
    for answer in answers[25:]: # 正解
        file.write('<td>' + answer +'</td>')
    file.write('</tr><tr>')
    for i in range(25,50): # 學生作答
        if student_answer[student][i] == answers[i]:
            file.write('<td>.</td>')
        else:
            file.write('<td>' + student_answer[student][i] + '</td>')
    
    student_image_path = os.path.join(".", "static", student + ".png")
    file.write('</tr></tbody></table></div><div class="row"><p class="h5"><strong>各向度分析：</strong></p><div class="row"><div class="col-6"><img class="img-fluid img-sm"  src="' + student_image_path + '">')
    file.write('</div><div class="col-6"><table class="table table-bordered text-center table-sm"><tbody><thead><tr class="table-secondary"><th>評定向度</th><th>得分／總分</th><th>得分率</th></tr></thead><tbody><tr>')
    file.write('<td>形音義</td>')
    file.write('<td>' + str(student_dict[student]["形音義"]) + '/' + str(class_dict["形音義"]) + '</td>')
    file.write('<td>' + str(round(student_dict[student]["形音義"] / class_dict["形音義"]*100 ,1)) + ' % </td>')
    file.write('</tr><tr>')
    file.write('<td>詞語使用</td>')
    file.write('<td>' + str(student_dict[student]["詞語使用"]) + '/' + str(class_dict["詞語使用"]) + '</td>')
    file.write('<td>' + str(round(student_dict[student]["詞語使用"] / class_dict["詞語使用"]*100, 1)) + ' % </td>')
    file.write('</tr><tr>')
    file.write('<td>成語運用</td>')
    file.write('<td>' + str(student_dict[student]["成語運用"]) + '/' + str(class_dict["成語運用"]) + '</td>')
    file.write('<td>' + str(round(student_dict[student]["成語運用"] / class_dict["成語運用"]*100, 1)) + ' % </td>')
    file.write('</tr><tr>')
    file.write('<td>修辭技巧</td>')
    file.write('<td>' + str(student_dict[student]["修辭技巧"]) + '/' + str(class_dict["修辭技巧"]) + '</td>')
    file.write('<td>' + str(round(student_dict[student]["修辭技巧"] / class_dict["修辭技巧"]*100, 1)) + ' % </td>')
    file.write('</tr><tr>')
    file.write('<td>國學常識</td>')
    file.write('<td>' + str(student_dict[student]["國學常識"]) + '/' + str(class_dict["國學常識"]) + '</td>')
    file.write('<td>' + str(round(student_dict[student]["國學常識"] / class_dict["國學常識"]*100, 1)) + ' % </td>')
    file.write('</tr><tr>')
    file.write('<td>閱讀素養</td>')
    file.write('<td>' + str(student_dict[student]["閱讀素養"]) + '/' + str(class_dict["閱讀素養"]) + '</td>')
    file.write('<td>' + str(round(student_dict[student]["閱讀素養"] / class_dict["閱讀素養"]*100, 1)) + ' % </td>')
    file.write('</tr><tr>')
    file.write('</tbody></table></div></div></div><div class="row"><p class="h5"><strong>本梯次成績統計：</strong></p><table class="table text-center table-bordered table-sm"><thead><tr class="table-secondary"><th>項目</th><th>分數</th><th>人數</th></tr></thead><tbody>')
    
    file.write('<tr>')
    file.write('<td>本梯次成績前２％分數</td>')
    if int(len(student_score)*0.02) == 0:
        file.write('<td>' + str(student_score[0][1]) + '</td>')
        file.write('<td>1</td>')
    else:
        file.write('<td>' + str(round(sum([s for _, s, _ in student_score[:int(len(student_score)*0.02)]]) / int(len(student_score)*0.02), 2)) + '</td>')
        file.write('<td>' + str(int(len(student_score)*0.02)) + '</td>')
    file.write('</tr><tr>')
    file.write('<td>高標（成績前５０％平均分數）</td>')
    file.write('<td>' + str(round(sum([s for _, s, _ in student_score[:int(len(student_score)*0.5)]]) / (len(student_score)*0.5), 2)) + '</td>')
    file.write('<td>' + str(int(len(student_score)*0.5)) + '</td>')
    file.write('</tr><tr>')
    file.write('<td>均標（成績平均分數）</td>')
    file.write('<td>' + str(round(sum([s for _, s, _ in student_score]) / len(student_score),2)) + '</td>')
    # file.write('<td>' + str(len(student_score)) + '</td>')
    file.write('<td>/</td>')
    file.write('</tr><tr>')
    file.write('<td>低標（成績後５０％平均分數）</td>')
    # file.write('<td>' + str(sum([s for _, s in student_score[int(len(student_score)*0.5):]]) / int(len(student_score)*0.5)) + '</td>')
    file.write('<td>' + str(round(sum([s for _, s, _ in student_score[int(len(student_score)*0.5):]]) / (len(student_score)*0.5), 2)) + '</td>')
    file.write('<td>' + str(int(len(student_score)*0.5)) + '</td>')
    file.write('</tr>')
    file.write('</tbody></table></div><div class="row"><p class="h5"><strong>應考學生整體成績排名：</strong></p><table class="table text-center table-bordered table-sm"><thead><tr class="table-secondary"><th>姓名</th><th>語文素養</th><th>名次</th></tr></thead><tbody>')

    for rank, (student1, score1, rank1) in enumerate(student_score):
        # 遮蔽名稱
        file.write('<tr><td>')
        if len(student1) == 1:
            file.write('Ｏ')
        else:
            file.write(student1[0])
            for char in student1[1:-1]:
                file.write('Ｏ')
            file.write(student1[-1])
        file.write('</td>')

        file.write('<td>' + str(score1) + '</td>')
        # file.write('<td>' + str(writing_score_dict[student1]) + '</td>')

        if rank1 <= one_third_rank:
            file.write('<td>' + str(rank1) + '</td>')
        else:
            file.write('<td></td>')

        file.write('</tr>')
    
    file.write('</tbody></table></div><p></p></div></body></html>')

    file.close()

# ====== make teacher html ====

student_score.sort(key=lambda x: x[2])

# time = exam_paper["第幾次"][0]  # 第 1 次全民中檢仿真模擬考
level = exam_paper["級別"][0]  # 級別：初等
date = exam_paper["測驗日期"][0]  # 級別：初等
for student, score, rank in student_score:
    file = open(os.path.join(output_path, "老師.html"), "w", encoding='utf-8')

    file.write('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>煜婷國文</title><link rel="stylesheet" href="./assets/css/bootstrap.min.css"></head> \
               <body><div class="container"><div class="row"> \
               <div class="col-8" style="padding-left: 0px !important">')
    
    # 標題
    file.write('<p class="h2"><strong>煜婷國文<br>第' + time + '次全民中檢仿真模擬考</strong></p>')
    file.write('</div><div class="col-4 text-right" style="padding-right: 0px !important">')
    file.write('<p class="h6">測驗日期：' + date.strftime("%Y/%m/%d") + '</p>')
    file.write('<p class="h6">檢定級別：' + level + '</p>')
    file.write('</div></div></div>')

    file.write('<div class="container">')
    file.write('<div class="row"><p class="h5"><strong>語文素養答題狀況：</strong></p>')
    file.write('<table class="table table-bordered text-center table-sm"><tbody><tr class="table-secondary">')
    for i in range(1,26): # 題號
        file.write('<td>' + str(i) +'</td>')
    file.write('</tr><tr>') 
    for class_ in classes[:25]: # 類別
        file.write('<td>' + class_[0] +'</td>')
    file.write('</tr><tr>') 
    for answer in answers[:25]: # 正解
        file.write('<td>' + answer +'</td>')
    file.write('</tr><tr style="font-size: 70% !important">')
    for idx in range(1, 26): # 正確率
        cor = int(100 - (question_dict[idx] / num_of_student * 100))
        if cor == 100:
            file.write('<td>-</td>')
        elif cor < 50:
            file.write('<td style="color: red">' + str(cor) + '%</td>')
        else:
            file.write('<td>' + str(cor) + '%</td>')
    file.write('</tr><tr>')
    for idx in range(1, 26): # 正確人數
        file.write('<td>' + str(num_of_student - question_dict[idx]) + '</td>')
    file.write('</tr>')

    file.write('<tr class="table-secondary">')
    for i in range(26,51): # 題號
        file.write('<td>' + str(i) +'</td>')
    file.write('</tr><tr>')
    for class_ in classes[25:]: # 類別
        file.write('<td>' + class_[0] +'</td>')
    file.write('</tr><tr>') 
    for answer in answers[25:]: # 正解
        file.write('<td>' + answer +'</td>')
    file.write('</tr><tr style="font-size: 70% !important">')
    for idx in range(26, 51): # 正確率
        cor = int(100 - (question_dict[idx] / num_of_student * 100))
        if cor == 100:
            file.write('<td>-</td>')
        elif cor < 50:
            file.write('<td style="color: red">' + str(cor) + '%</td>')
        else:
            file.write('<td>' + str(cor) + '%</td>')
    file.write('</tr><tr>')
    for idx in range(26, 51): # 正確人數
        file.write('<td>' + str(num_of_student - question_dict[idx]) + '</td>')
    
    teacher_image_path = os.path.join(".", "static", "給老師看的.png")
    file.write('</tr></tbody></table></div><div class="row"><p class="h5"><strong>各向度分析：</strong></p><div class="row"><div class="col-6"><img class="img-fluid img-sm"  src="' + teacher_image_path + '">')
    file.write('</div><div class="col-6"><table class="table table-bordered text-center table-sm"><tbody><thead><tr class="table-secondary"><th>評定向度</th><th>該向度題數</th><th>正確率</th></tr></thead><tbody><tr>')
    file.write('<td>形音義</td>')
    file.write('<td>' + str(class_dict["形音義"]) + ' 題</td>')
    file.write('<td>' + str(round(class_dict["形音義"] - wrong_dict["形音義"] / num_of_student, 2))+" 題／人")
    file.write('</tr><tr>')
    file.write('<td>詞語使用</td>')
    file.write('<td>' + str(class_dict["詞語使用"]) + ' 題</td>')
    file.write('<td>' + str(round(class_dict["詞語使用"] - wrong_dict["詞語使用"] / num_of_student, 2))+" 題／人")
    file.write('</tr><tr>')
    file.write('<td>成語運用</td>')
    file.write('<td>' + str(class_dict["成語運用"]) + ' 題</td>')
    file.write('<td>' + str(round(class_dict["成語運用"] - wrong_dict["成語運用"] / num_of_student, 2))+" 題／人")
    file.write('</tr><tr>')
    file.write('<td>修辭技巧</td>')
    file.write('<td>' + str(class_dict["修辭技巧"]) + ' 題</td>')
    file.write('<td>' + str(round(class_dict["修辭技巧"] - wrong_dict["修辭技巧"] / num_of_student, 2))+" 題／人")
    file.write('</tr><tr>')
    file.write('<td>國學常識</td>')
    file.write('<td>' + str(class_dict["國學常識"]) + ' 題</td>')
    file.write('<td>' + str(round(class_dict["國學常識"] - wrong_dict["國學常識"] / num_of_student, 2))+" 題／人")
    file.write('</tr><tr>')
    file.write('<td>閱讀素養</td>')
    file.write('<td>' + str(class_dict["閱讀素養"]) + ' 題</td>')
    file.write('<td>' + str(round(class_dict["閱讀素養"] - wrong_dict["閱讀素養"] / num_of_student, 2))+" 題／人")
    file.write('</tr><tr>')
    file.write('</tbody></table></div></div></div><div class="row"><p class="h5"><strong>本梯次成績統計：</strong></p><table class="table text-center table-bordered table-sm"><thead><tr class="table-secondary"><th>項目</th><th>分數</th><th>人數</th></tr></thead><tbody>')
    
    file.write('<tr>')
    file.write('<td>本梯次成績前２％分數</td>')
    if int(len(student_score)*0.02) == 0:
        file.write('<td>' + str(student_score[0][1]) + '</td>')
        file.write('<td>1</td>')
    else:
        file.write('<td>' + str(round(sum([s for _, s, _ in student_score[:int(len(student_score)*0.02)]]) / int(len(student_score)*0.02), 2)) + '</td>')
        file.write('<td>' + str(int(len(student_score)*0.02)) + '</td>')
    file.write('</tr><tr>')
    file.write('<td>高標（成績前５０％平均分數）</td>')
    file.write('<td>' + str(round(sum([s for _, s, _ in student_score[:int(len(student_score)*0.5)]]) / (len(student_score)*0.5), 2)) + '</td>')
    file.write('<td>' + str(int(len(student_score)*0.5)) + '</td>')
    file.write('</tr><tr>')
    file.write('<td>均標（成績平均分數）</td>')
    file.write('<td>' + str(round(sum([s for _, s, _ in student_score]) / len(student_score),2)) + '</td>')
    # file.write('<td>' + str(len(student_score)) + '</td>')
    file.write('<td>/</td>')
    file.write('</tr><tr>')
    file.write('<td>低標（成績後５０％平均分數）</td>')
    # file.write('<td>' + str(sum([s for _, s in student_score[int(len(student_score)*0.5):]]) / int(len(student_score)*0.5)) + '</td>')
    file.write('<td>' + str(round(sum([s for _, s, _ in student_score[int(len(student_score)*0.5):]]) / (len(student_score)*0.5), 2)) + '</td>')
    file.write('<td>' + str(int(len(student_score)*0.5)) + '</td>')
    file.write('</tr>')
    file.write('</tbody></table></div><div class="row"><p class="h5"><strong>應考學生整體成績排名：</strong></p><table class="table text-center table-bordered table-sm"><thead><tr class="table-secondary"><th>姓名</th><th>語文素養</th><th>名次</th></tr></thead><tbody>')

    for rank, (student1, score1, rank1) in enumerate(student_score):

        # 遮蔽名稱
        file.write('<tr><td>')
        if len(student1) == 1:
            file.write('Ｏ')
        else:
            file.write(student1[0])
            for char in student1[1:-1]:
                file.write('Ｏ')
            file.write(student1[-1])
        file.write('</td>')

        # 語文素養成績        
        file.write('<td>' + str(score1) + '</td>')
        # file.write('<td>' + str(writing_score_dict[student1]) + '</td>')

        file.write('<td>' + str(rank1) + '</td>')

        file.write('</tr>')
    
    file.write('</tbody></table></div><p></p></div></body></html>')

    file.close()