"""
008课件练习题
按照100分制，90分以上成绩为A,80到90为B，60到80为C，60以下为D。当用户
输入分数，自动转换为ABCD的形式打出
"""
score=input("请键入分数：")
score=int(score)
if score>=90:
    print("A")
if 80<=score<90:
    print("B")
if 60<=score<80:
    print("C")
if  score<60:
    print("D")
