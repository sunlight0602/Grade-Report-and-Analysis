import pandas as pd
import xlsxwriter
import matplotlib.pyplot as plt
import numpy as np

# Set matplotlib parameters
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] # 用於正常顯示中文
plt.rcParams['axes.unicode_minus'] = False # 用於正常顯示符號
plt.style.use('ggplot') # 使用ggplot的繪圖風格，這個類似於美化了

# File path:
output_path = '.\\output_files\\'
html_path = '.\\output_files\\成績單\\'
input_path = ".\\input_files\\"

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
    ax.set_thetagrids(angles=(0,72,144,216,288), labels=class_dict.keys(), fontsize=14)

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
    ax.set_thetagrids(angles=(0,72,144,216,288), labels=wrong_dict.keys(), fontsize=14)

    ax.set_ylim(0, 100) # 設置雷達圖的範圍
    ax.grid(True) # 添加網格線

    plt.savefig(output_path + "給老師看的.png")


# Read files
exam_paper = pd.read_excel(input_path + "閱讀素養題目.xlsx")
student_answer = pd.read_excel(input_path + "學生閱讀素養答案.xlsx", converters={'學生/題號': int})
speed = pd.read_excel(input_path + "作答速度.xlsx")
bubbles = pd.read_excel(input_path + "學生劃卡狀況.xlsx")

# Regularize data
speed_dict = {}
bubbles_dict = {}
for i in range(len(speed)):
    name = speed['學生'][i]
    speeds = []
    for j in range(1,6):
        temp = speed['作答速度'+str(j)][i]
        if not pd.isnull(temp):
            speeds.append(speed['作答速度'+str(j)][i])
    speed_dict[name] = speeds
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
# print(student_answer["冠妤"][69])
# print(class_dict)
student_score = []

for i in range(num_of_student):
    student_name = student_answer.columns[i+1]
    print('學生名稱:', student_name)

    workbook = xlsxwriter.Workbook(output_path + student_name + '.xlsx')
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
    for question, answer, class_ in zip(questions, answers, classes):
        worksheet.write(row, 0, question)
        worksheet.write(row, 1, class_)
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
    draw_fig(student_name, class_dict, student_dict[student_name])

# ==== Make Excel workbook ====

workbook = xlsxwriter.Workbook(output_path + '給老師看的.xlsx')
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

# ======= Make HTML ==========

# Get first three places:
first_place = student_score[0][1]
second_place = 0
for _, score in student_score[1:]:
    second_place = score
    if second_place != first_place:
        break
third_place = 0
for _, score in student_score[1:]:
    third_place = score
    if third_place != second_place:
        if third_place != first_place:
            break

import random
student_score_randomed = random.shuffle(student_score)

time = exam_paper["第幾次"][0]  # 第 1 次全民中檢仿真模擬考
level = exam_paper["級別"][0]  # 級別：初等
date = exam_paper["測驗日期"][0]  # 級別：初等
for student, score in student_score:
    file = open(html_path + student + "_html.html", "w", encoding='utf-8')

    file.write('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>煜婷國文</title><link rel="stylesheet" href="./assets/css/bootstrap.min.css"></head><body><div class="container"><div class="row">')
    file.write('<div class="col-8" style="padding-left: 0px !important">')
    file.write('<p class="h2"><strong>煜婷國文<br>')
    # file.write('第' + time + '次')
    file.write('五年級語文能力檢測')
    file.write('</strong></p>')
    file.write('</div><div class="col-4 text-right" style="padding-right: 0px !important">')
    file.write('<p class="h6">測驗日期：' + date.strftime("%Y/%m/%d") + '</p>')
    # file.write('<p class="h6">檢定級別：' + level + '</p>')
    file.write('</div></div><div class="row"><p class="h5"><strong>總體成績概要：</strong></p><table class="table text-center table-bordered table-sm"><thead><tr class="table-secondary">')

    file.write('<th>姓名</th>')
    file.write('<th>分數</th>')
    file.write('<th>應考人數</th>')
    file.write('<th>作答速度</th>')
    file.write('<th>畫卡狀況</th>')
    file.write('</tr></thead><tbody><tr>')

    file.write('<td class="align-middle">' + student + '</td>')
    file.write('<td class="align-middle">' + str(score) + '</td>')
    file.write('<td class="align-middle">' + str(num_of_student) + '人</td>')

    file.write('<td class="align-left"><div class="row align-left"><div class="col text-left ml-5">')
    if "表現良好" in speed_dict[student]:
        file.write('☑ 表現良好<br>')
    else:
        file.write('☐ 表現良好<br>')
    if "可再加快" in speed_dict[student]:
        file.write('☑ 可再加快<br>')
    else:
        file.write('☐ 可再加快<br>')
    if "未完成，須提升作答速度" in speed_dict[student]:
        file.write('☑ 未完成，須提升作答速度<br>')
    else:
        file.write('☐ 未完成，須提升作答速度<br>')
    if "違反考試規則" in speed_dict[student]:
        file.write('☑ 違反考試規則<br>')
    else:
        file.write('☐ 違反考試規則<br>')
    if "容易分心，專注度待加強" in speed_dict[student]:
        file.write('☑ 容易分心，專注度待加強<br>')
    else:
        file.write('☐ 容易分心，專注度待加強<br>')
    if "作答速度快，但沒有檢查習慣" in speed_dict[student]:
        file.write('☑ 作答速度快，但沒有檢查習慣<br>')
    else:
        file.write('☐ 作答速度快，但沒有檢查習慣<br>')
    file.write('</div></row></td>')

    file.write('<td class="align-middle"><div class="row align-middle"><div class="col align-left">')
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
    file.write('</div></row></td>')
    file.write('</tr></tbody></table>')

    file.write('<p>試題共６０題，總分１２０分。作答時間４０分鐘。</p>')
    file.write('</div><div class="row"><p class="h5"><strong>語文素養答題狀況：</strong></p><table class="table table-bordered text-center table-sm"><tbody><tr class="table-secondary">')
    
    # 1~25 題
    NUMROW1 = 30
    for i in range(1, NUMROW1+1): # 題號
        file.write('<td>' + str(i) +'</td>')
    file.write('</tr><tr>') 
    for answer in answers[:NUMROW1]: # 正解
        file.write('<td>' + answer +'</td>')
    file.write('</tr><tr>')
    for i in range(0, NUMROW1): # 學生作答
        if student_answer[student][i] == answers[i]:
            file.write('<td>.</td>')
        else:
            file.write('<td>' + str(student_answer[student][i]) + '</td>')
    file.write('</tr>')

    # 26~50 題
    NUMROW2 = 60
    file.write('<tr class="table-secondary">')
    for i in range(NUMROW1+1, NUMROW2+1): # 題號
        file.write('<td>' + str(i) +'</td>')
    file.write('</tr><tr>')
    for answer in answers[NUMROW1:]: # 正解
        file.write('<td>' + answer +'</td>')
    file.write('</tr><tr>')
    for i in range(NUMROW1, NUMROW2): # 學生作答
        if student_answer[student][i] == answers[i]:
            file.write('<td>.</td>')
        else:
            file.write('<td>' + str(student_answer[student][i]) + '</td>')
    
    # Image
    file.write('</tr></tbody></table></div><div class="row"><p class="h5"><strong>各向度分析：</strong></p><div class="row"><div class="col-6"><img class="img-fluid img-sm"  src="..\\' + student + '.png">')

    # Detail Table
    file.write('</div><div class="col-6"><table class="table table-bordered text-center table-sm"><tbody><thead><tr class="table-secondary"><th>評定向度</th><th>答對題數／題數</th><th>得分率</th></tr></thead><tbody><tr>')
    file.write('<td>閱讀單題</td>')
    file.write('<td>' + str(student_dict[student]["閱讀單題"]) + '/' + str(class_dict["閱讀單題"]) + '</td>')
    file.write('<td>' + str(round(student_dict[student]["閱讀單題"] / class_dict["閱讀單題"]*100 ,1)) + ' % </td>')
    file.write('</tr><tr>')
    file.write('<td>閱讀題組</td>')
    file.write('<td>' + str(student_dict[student]["閱讀題組"]) + '/' + str(class_dict["閱讀題組"]) + '</td>')
    file.write('<td>' + str(round(student_dict[student]["閱讀題組"] / class_dict["閱讀題組"]*100 ,1)) + ' % </td>')   
    file.write('</tr><tr>')
    file.write('<td>形音義</td>')
    file.write('<td>' + str(student_dict[student]["形音義"]) + '/' + str(class_dict["形音義"]) + '</td>')
    file.write('<td>' + str(round(student_dict[student]["形音義"] / class_dict["形音義"]*100 ,1)) + ' % </td>')
    file.write('</tr><tr>')
    file.write('<td>成語應用</td>')
    file.write('<td>' + str(student_dict[student]["成語應用"]) + '/' + str(class_dict["成語應用"]) + '</td>')
    file.write('<td>' + str(round(student_dict[student]["成語應用"] / class_dict["成語應用"]*100, 1)) + ' % </td>')
    file.write('</tr><tr>')
    file.write('<td>國學常識</td>')
    file.write('<td>' + str(student_dict[student]["國學常識"]) + '/' + str(class_dict["國學常識"]) + '</td>')
    file.write('<td>' + str(round(student_dict[student]["國學常識"] / class_dict["國學常識"]*100, 1)) + ' % </td>')
    file.write('</tr><tr>')
    file.write('</tbody></table></div></div></div><div class="row"><p class="h5"><strong>本梯次成績統計：</strong></p><table class="table text-center table-bordered table-sm"><thead><tr class="table-secondary"><th>項目</th><th>分數</th><th>人數</th></tr></thead><tbody>')
    
    file.write('<tr>')
    file.write('<td>本梯次成績前２％分數</td>')
    if int(len(student_score)*0.02) == 0:
        file.write('<td>' + str(student_score[0][1]) + '</td>')
        file.write('<td>1</td>')
    else:
        file.write('<td>' + str(round(sum([s for _, s in student_score[:int(len(student_score)*0.02)]]) / int(len(student_score)*0.02), 2)) + '</td>')
        file.write('<td>' + str(int(len(student_score)*0.02)) + '</td>')
    file.write('</tr><tr>')
    file.write('<td>高標（成績前５０％平均分數）</td>')
    file.write('<td>' + str(round(sum([s for _, s in student_score[:int(len(student_score)*0.5)]]) / (len(student_score)*0.5), 2)) + '</td>')
    file.write('<td>' + str(int(len(student_score)*0.5)) + '</td>')
    file.write('</tr><tr>')
    file.write('<td>均標（成績平均分數）</td>')
    file.write('<td>' + str(round(sum([s for _, s in student_score]) / len(student_score),2)) + '</td>')
    file.write('<td>' + str(len(student_score)) + '</td>')
    file.write('</tr><tr>')
    file.write('<td>低標（成績後５０％平均分數）</td>')
    # file.write('<td>' + str(sum([s for _, s in student_score[int(len(student_score)*0.5):]]) / int(len(student_score)*0.5)) + '</td>')
    file.write('<td>' + str(round(sum([s for _, s in student_score[int(len(student_score)*0.5):]]) / (len(student_score)*0.5), 2)) + '</td>')
    file.write('<td>' + str(int(len(student_score)*0.5)) + '</td>')
    file.write('</tr>')
    file.write('</tbody></table></div>')

    # Move 排名 to page 2
    file.write('<br><br>')

    # 排名
    file.write('<div class="row"><p class="h5"><strong>應考學生整體成績排名：</strong></p><table class="table text-center table-bordered table-sm"><thead><tr class="table-secondary"><th>姓名</th><th>分數</th>')
    file.write('<th>名次</th></tr></thead><tbody>')
    for rank, (student1, score1) in enumerate(student_score):
        file.write('<tr>')
        if len(student1) == 3:
            file.write('<td>' + student1[0] + 'Ｏ' + student1[2] + '</td>')
        elif len(student1) == 2:
            file.write('<td>' + student1[0] + 'Ｏ'  + '</td>')
        else:
            file.write('<td>')
            file.write(student1[0])
            for i in range(len(student1)-2):
                file.write('Ｏ')
            file.write(student1[-1])
            file.write('</td>') # bug here
        file.write('<td>' + str(score1) + '</td>')
        # file.write('<td>' + str(writing_score_dict[student1]) + '</td>')

        if score1 == first_place:
            file.write('<td>1</td>')
        elif score1 == second_place:
            file.write('<td>2</td>')
        elif score1 == third_place:
            file.write('<td>3</td>')
        else:
            file.write('<td></td>')

        file.write('</tr>')
    
    file.write('</tbody></table></div><p></p></div></body></html>')

    file.close()

# ====== make teacher html ====
# ====== make teacher html ====
# ====== make teacher html ====

student_score.sort(key=lambda x: x[1], reverse=True)
temp = -1
rk = 0
for idx, (name, score) in enumerate(student_score):
    if score != temp:
        rk += 1
    student_score[idx] += (rk,)
    temp = score
    
print(student_score)

# time = exam_paper["第幾次"][0]  # 第 1 次全民中檢仿真模擬考
# level = exam_paper["級別"][0]  # 級別：初等
date = exam_paper["測驗日期"][0]
for student, score, rk in student_score:
    file = open(html_path + "給老師看的_html.html", "w", encoding='utf-8')

    file.write('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>煜婷國文</title><link rel="stylesheet" href="./assets/css/bootstrap.min.css"></head>')
    file.write('<body><div class="container"><div class="row">')
    file.write('<div class="col-8" style="padding-left: 0px !important">')
    file.write('<p class="h2"><strong>煜婷國文<br>')
    # file.write('第' + time + '次')
    file.write('五年級語文能力檢測</strong></p>')
    file.write('</div><div class="col-4 text-right" style="padding-right: 0px !important">')
    file.write('<p class="h6">測驗日期：' + date.strftime("%Y/%m/%d") + '</p>')
    # file.write('<p class="h6">檢定級別：' + level + '</p>')
    file.write('</div></div></div>')

    # 答題狀況
    file.write('<div class="container">')
    file.write('<div class="row"><p class="h5"><strong>語文素養答題狀況：</strong></p>')
    file.write('<table class="table table-bordered text-center table-sm"><tbody><tr class="table-secondary">')
    for i in range(1, NUMROW1+1): # 題號
        file.write('<td>' + str(i) +'</td>')
    file.write('</tr><tr>') 
    for class_ in classes[:NUMROW1]: # 類別
        file.write('<td>' + class_[0] +'</td>')
    file.write('</tr><tr>') 
    for answer in answers[:NUMROW1]: # 正解
        file.write('<td>' + answer +'</td>')
    file.write('</tr><tr style="font-size: 70% !important">')
    for idx in range(1, NUMROW1+1): # 正確率
        cor = int(100 - (question_dict[idx] / num_of_student * 100))
        if cor == 100:
            file.write('<td>-</td>')
        elif cor < 50:
            file.write('<td style="color: red">' + str(cor) + '%</td>')
        else:
            file.write('<td>' + str(cor) + '%</td>')
    file.write('</tr><tr>')
    for idx in range(1, NUMROW1+1): # 正確人數
        file.write('<td>' + str(num_of_student - question_dict[idx]) + '</td>')
    file.write('</tr>')

    file.write('<tr class="table-secondary">')
    for i in range(NUMROW1+1, NUMROW2+1): # 題號
        file.write('<td>' + str(i) +'</td>')
    file.write('</tr><tr>')
    for class_ in classes[NUMROW1:]: # 類別
        file.write('<td>' + class_[0] +'</td>')
    file.write('</tr><tr>') 
    for answer in answers[NUMROW1:]: # 正解
        file.write('<td>' + answer +'</td>')
    file.write('</tr><tr style="font-size: 70% !important">')
    for idx in range(NUMROW1+1, NUMROW2+1): # 正確率
        cor = int(100 - (question_dict[idx] / num_of_student * 100))
        if cor == 100:
            file.write('<td>-</td>')
        elif cor < 50:
            file.write('<td style="color: red">' + str(cor) + '%</td>')
        else:
            file.write('<td>' + str(cor) + '%</td>')
    file.write('</tr><tr>')
    for idx in range(NUMROW1+1, NUMROW2+1): # 正確人數
        file.write('<td>' + str(num_of_student - question_dict[idx]) + '</td>')
    
    # Image
    file.write('</tr></tbody></table></div><div class="row"><p class="h5"><strong>各向度分析：</strong></p><div class="row"><div class="col-6"><img class="img-fluid img-sm"  src="..\\給老師看的.png">')
    
    # Detailed Table
    file.write('</div><div class="col-6"><table class="table table-bordered text-center table-sm"><tbody><thead><tr class="table-secondary"><th>評定向度</th><th>該向度題數</th><th>正確率</th></tr></thead><tbody><tr>')
    file.write('<td>閱讀單題</td>')
    file.write('<td>' + str(class_dict["閱讀單題"]) + ' 題</td>')
    file.write('<td>' + str(round(class_dict["閱讀單題"] - wrong_dict["閱讀單題"] / num_of_student, 2))+" 題／人")
    file.write('</tr><tr>')
    file.write('<td>閱讀題組</td>')
    file.write('<td>' + str(class_dict["閱讀題組"]) + ' 題</td>')
    file.write('<td>' + str(round(class_dict["閱讀題組"] - wrong_dict["閱讀題組"] / num_of_student, 2))+" 題／人")
    file.write('</tr><tr>')
    file.write('<td>形音義</td>')
    file.write('<td>' + str(class_dict["形音義"]) + ' 題</td>')
    file.write('<td>' + str(round(class_dict["形音義"] - wrong_dict["形音義"] / num_of_student, 2))+" 題／人")
    file.write('</tr><tr>')
    file.write('<td>成語應用</td>')
    file.write('<td>' + str(class_dict["成語應用"]) + ' 題</td>')
    file.write('<td>' + str(round(class_dict["成語應用"] - wrong_dict["成語應用"] / num_of_student, 2))+" 題／人")
    file.write('</tr><tr>')
    file.write('<td>國學常識</td>')
    file.write('<td>' + str(class_dict["國學常識"]) + ' 題</td>')
    file.write('<td>' + str(round(class_dict["國學常識"] - wrong_dict["國學常識"] / num_of_student, 2))+" 題／人")
    file.write('</tr><tr>')
    file.write('</tbody></table></div></div></div><div class="row"><p class="h5"><strong>本梯次成績統計：</strong></p><table class="table text-center table-bordered table-sm"><thead><tr class="table-secondary"><th>項目</th><th>分數</th><th>人數</th></tr></thead><tbody>')
    
    file.write('<tr>')
    file.write('<td>本梯次成績前２％分數</td>')
    if int(len(student_score)*0.02) == 0:
        file.write('<td>' + str(student_score[0][1]) + '</td>')
        file.write('<td>1</td>')
    else:
        file.write('<td>' + str(round(sum([s for _, s in student_score[:int(len(student_score)*0.02)]]) / int(len(student_score)*0.02), 2)) + '</td>')
        file.write('<td>' + str(int(len(student_score)*0.02)) + '</td>')
    file.write('</tr><tr>')
    file.write('<td>高標（成績前５０％平均分數）</td>')
    file.write('<td>' + str(round(sum([s for _, s, _ in student_score[:int(len(student_score)*0.5)]]) / (len(student_score)*0.5), 2)) + '</td>')
    file.write('<td>' + str(int(len(student_score)*0.5)) + '</td>')
    file.write('</tr><tr>')
    file.write('<td>均標（成績平均分數）</td>')
    file.write('<td>' + str(round(sum([s for _, s, _ in student_score]) / len(student_score),2)) + '</td>')
    file.write('<td>' + str(len(student_score)) + '</td>')
    file.write('</tr><tr>')
    file.write('<td>低標（成績後５０％平均分數）</td>')
    # file.write('<td>' + str(sum([s for _, s in student_score[int(len(student_score)*0.5):]]) / int(len(student_score)*0.5)) + '</td>')
    file.write('<td>' + str(round(sum([s for _, s, _ in student_score[int(len(student_score)*0.5):]]) / (len(student_score)*0.5), 2)) + '</td>')
    file.write('<td>' + str(int(len(student_score)*0.5)) + '</td>')
    file.write('</tr>')
    file.write('</tbody></table></div>')

    file.write('<div class="row">')
    file.write('<p class="h5"><strong>應考學生整體成績排名：</strong></p>')
    file.write('</div>')

    file.write('<div class="row">')

    file.write('<div class="col-6">')
    file.write('<table class="table text-center table-bordered table-sm"><thead><tr class="table-secondary"><th>姓名</th><th>分數</th>')
    file.write('<th>名次</th></tr></thead>')
    file.write('<tbody>')
    for student1, score1, rank1 in student_score[:8]:
        file.write('<tr>')
        file.write('<td>' + student1 + '</td>')
        file.write('<td>' + str(score1) + '</td>')
        # file.write('<td>' + str(writing_score_dict[student1]) + '</td>')
        file.write('<td>' + str(rank1) + '</td>')
        file.write('</tr>')
    file.write('</tbody></table></div>') # div for col

    file.write('<div class="col-6">')
    file.write('<table class="table text-center table-bordered table-sm"><thead><tr class="table-secondary"><th>姓名</th><th>分數</th>')
    file.write('<th>名次</th></tr></thead><tbody>')
    for student1, score1, rank1 in student_score[8:]:
        file.write('<tr>')
        file.write('<td>' + student1 + '</td>')
        file.write('<td>' + str(score1) + '</td>')
        # file.write('<td>' + str(writing_score_dict[student1]) + '</td>')
        file.write('<td>' + str(rank1) + '</td>')
        file.write('</tr>')
    file.write('</tbody></table></div>')
    file.write('</div>') # div for row
    file.write('</body></html>')

    file.close()