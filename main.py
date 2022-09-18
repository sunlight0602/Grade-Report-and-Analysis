import pandas as pd
import xlsxwriter
from draw_fig import draw_fig

# File path:
output_path = '.\/output_files\/'
input_path = ".\/input_files\/"

# Read files
exam_paper = pd.read_excel(input_path + "exam_paper.xlsx")
student_answer = pd.read_excel(input_path + "student_answer.xlsx", converters={'學生/題號': int})

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
        student_dict[class_] = 0 # Class: 0
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
    
    for class_ in student_dict.keys():
        student_dict[class_] = 0

    correct = 0
    row = 1
    for question, answer, class_ in zip(questions, answers, classes):
        worksheet.write(row, 0, question)
        worksheet.write(row, 1, class_)
        if student_answer[student_name][question-1] == answer:
            worksheet.write(row, 2, "O")
            correct += 1
            student_dict[class_] += 1
        else:
            worksheet.write(row, 2, "X")
            question_dict[question] += 1
            wrong_dict[class_] += 1
        row += 1
        
    for idx, class_  in enumerate(class_dict.keys()):
        worksheet.write(1, 3+idx, str(student_dict[class_]) + '/' + str(class_dict[class_]))
    
    print('分數:', int(correct / num_of_question * 100))
    workbook.close()

    student_score.append((student_name, int(correct / num_of_question * 100)))

    # =====

    print(student_dict)
    draw_fig(student_name, class_dict, student_dict)

# ====

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

student_score.sort(key=lambda x: x[1], reverse=True)
print(student_score)
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
worksheet.write(3, 6, sum([s for _, s in student_score]) / int(len(student_score)))
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