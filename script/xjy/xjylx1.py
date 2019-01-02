import time
from time import *
print('------------------------我爱python--------------------')
temp=input("不妨猜一下小甲鱼现在心里想的是哪个数字：")
guess=int(temp)
if guess==8:
    sleep(2)
    print("你是小甲鱼心里的蛔虫吗？！")
    sleep(3)
    print("猜对了也没有奖励！")
else:
    print("猜错了，小甲鱼现在心里想的是8！")
print("游戏结束，不玩啦^_^")
