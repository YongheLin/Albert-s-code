import random
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

data = np.loadtxt("data.txt")


class SA:
    def __init__(self,T0=100,Tf=0.01,alpha=0.99,iter=100):
        self.T0 = T0     # 初始温度100
        self.T = T0      # 当前温度T
        self.Tf = Tf     # 终值温度0.01
        self.alpha = alpha  # 冷却系数0.99
        self.iter = iter    # 内循环迭代次数为100
        self.x = data[:,0]; # 初始x数组
        self.y = data[:,1]; # 初始y数组
        self.best = [0 for i in range(len(data))]      # 存储最优解
        self.vis = [False for i in range(len(data))]

        self.history = {'d':[],'T':[]}


    # 初始化最优解
    def initial(self):
        count = 0
        while count<len(data):
            ind = np.random.randint(0,len(data))
            if not self.vis[ind]:
                self.best[count] = ind
                self.vis[ind] = True
                count += 1


    # 计算距离
    def distance(self,x,y):
        d = 0;
        for i in range(1,len(data)):
            dx = (x[i]-x[i-1])**2
            dy = (y[i]-y[i-1])**2
            d += math.sqrt(dx+dy)
        d0 = math.sqrt((x[len(data)-1]-x[0])**2+(y[len(data)-1]-y[0])**2)
        d += d0
        return d


    # 随机生成要交换的城市
    def generate(self,i):
        while True:
            new_i = i+np.random.randint(-len(data),len(data));
            if new_i<len(data) and new_i>=0:
                break;
        return new_i;


    # 判断是否接受新解
    def Metrospolits(self,d,new_d):
        if new_d <= d:
            return 1
        else:
            p = np.exp((d-new_d)/self.T)
            if random.random() < p:
                return 1
            else:
                return 0


    def run(self):
        count = 0
        self.initial();
        while self.T>self.Tf:
            for i in range(self.iter):
                d = self.distance(self.x,self.y)
                while True:
                    ind = np.random.randint(0,len(data))
                    new_ind = np.random.randint(0,len(data))
                    if i!=new_ind:
                        break
                cx = self.x.copy()
                cy = self.y.copy()

                temp_x = cx[ind]
                cx[ind] = cx[new_ind]
                cx[new_ind] = temp_x
                temp_y = cy[ind]
                cy[ind] = cy[new_ind]
                cy[new_ind] = temp_y

                new_d = self.distance(cx,cy)
                if self.Metrospolits(d,new_d):
                    self.x = cx;
                    self.y = cy;
                    temp_b = self.best[ind]
                    self.best[ind] = self.best[new_ind]
                    self.best[new_ind] = temp_b

            d = self.distance(self.x,self.y)
            self.history['d'].append(d)
            self.history['T'].append(self.T)

            self.T = self.T*self.alpha
            count += 1

        min_d = min(self.history['d'])
        best_path = self.best
        print("最优路径为:{0},\n,最短距离为:{1}\n".format(best_path,min_d))

sa = SA()
sa.run()
