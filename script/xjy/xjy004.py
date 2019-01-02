"""
004改进小游戏
1、猜错后提醒用户是猜大了还是才小了
"""
"""number=input("猜小甲鱼现在想的什么数字，请输入：")
num=int(number)
if num==8:
    print("猜对了，你是小甲鱼心里的蛔虫吗？")
else:
    if num>8:
        print("哥们，大了大了~~")
    else:
        print("嘿，小了小了")
print("游戏结束")
"""


"""
改进二，程序应该提供多次机会给用户猜测，程序需要重复运行一些代码
猜错三次结束
"""
i=0   # 循环次数i，初始值为1
number=input("猜小甲鱼现在想的什么数字,你有三次机会，请输入：")
num=int(number)
while i<2 :
    i=i+1
    if num==8:
        print("恭喜猜对了，你是小甲鱼心里的蛔虫吗？")
        break
    if num<8:
        print("小了，小了")
    else:
        print("大了，大了")
    number=input("请重新输入，还有"+str(3-i)+"次机会：")
    num=int(number)
print("游戏结束，不玩了")
    

"""
第三个改进要求，每次运行程序产生的答案是随机的
引入random模块
"""
import random
secret=random.randint(1,10)  #生成1到10之间的随机数
number=input("请猜测小甲鱼心里现在想的什么数字，你有三次机会，请输入：")
num=int(number)
for y in (0,1):  # 依次将0,1赋值给y
    if num==secret:
        print("恭喜你答对了，你是小甲鱼心里的蛔虫吗？")
        break
    if num<secret:
        print("小了，小了")
    else:
        print("大了，大了")
    number=input("请重新输入，还有"+str(2-y)+"次机会：")
    num=int(number)
print("游戏结束，不玩了")
