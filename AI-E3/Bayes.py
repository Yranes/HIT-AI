import numpy as np

class cpt:
    def __init__(self, name, parents, probabilities):
        self.name = name
        self.parents = parents
        self.probabilities = probabilities

All = []

def Dfs(nums, Event, now):
    if now >= nums:
        global All
        All.append(Event)
        return 
    if Event[now] >= 3: #是未被确定0/1的位置
        new_Event = list(Event)
        new_Event[now] = 0
        Dfs(nums, new_Event, now + 1)
        New_Event = list(Event)
        New_Event[now] = 1
        Dfs(nums, New_Event, now + 1)
    else:
        Dfs(nums, Event, now + 1) #0/1已经被确定了

class BN:
    def __init__(self, nums, variables, graph, cpts):
        self.nums = nums
        self.cpts = cpts
        self.graph = graph
        self.variables = variables
        self.TotalProbability = self.CalculateTotalProbability()

    def int2bi(self, num): # 将十进制数转换为01序列（2进制）
        List = []
        while num != 0:
            List.insert(0, num % 2)
            num //= 2
        Add_zero = self.nums - len(List)
        for i in range(Add_zero):
            List.insert(0, 0) # 需要补0保证长度
        return List

    def All_p(self, Event): # 调用dfs函数，求全部可能01序列
        global All
        All = []
        Dfs(self.nums, Event, 0)
        return All

    def bi2int(self, List): #将01序列转换为十进制数
        val, b = 0, 1
        for i in range(len(List) - 1, -1, -1):
            val += List[i] * b
            b *= 2
        return val

    def CalculateProbability(self, event): #计算条件概率
        Every_3 = [3 if i == 3 else 0 for i in event]
        Every_0_1 = [i if i == 1 or i == 0 else 0 for i in event]

        p1 = 0 # p1为变量为True下的条件概率
        Every_2 = [1 if i == 2 else 0 for i in event] #先给对应位置赋值1 (求 p = True的条件概率)
        Every_2_fan = [0 for i in event] # 后求(p = false的条件概率)

        Event = [Every_3[i] + Every_0_1[i] + Every_2[i] for i in range(self.nums)]

        Ap = self.All_p(Event) # dfs计算所有可能的01序列
        for Pos in Ap:
            index = self.bi2int(Pos)
            p1 += self.TotalProbability[index]

        Event = [Every_3[i] + Every_0_1[i] + Every_2_fan[i] for i in range(self.nums)]

        p0 = 0 # p0为变量为false下的条件概率
        Ap = self.All_p(Event)
        for Pos in Ap:
            index = self.bi2int(Pos)
            p0 += self.TotalProbability[index]
        
        Sum = p0 + p1 # 归一化
        return [p1 / Sum, p0 / Sum]

    def CalculateTotalProbability(self): # 计算全部联合概率
        TotalProbability = [0 for i in range(2 ** self.nums)]
        for i in range(2 ** self.nums):
            p = 0
            b_list = self.int2bi(i)
            for j in range(self.nums):
                if self.cpts[j].parents == []:
                    if(self.cpts[j].probabilities[0][1 - b_list[j]] != 0):
                        p += np.log2(self.cpts[j].probabilities[0][1 - b_list[j]])
                    else:
                        p = None
                        break
                else:
                    index, k_2 = 0, 1
                    parents = list(reversed(self.cpts[j].parents))
                    for parent in parents:
                        index += b_list[parent] * k_2
                        k_2 *= 2
                    if(self.cpts[j].probabilities[index][1 - b_list[j]] != 0):
                        p += np.log2(self.cpts[j].probabilities[0][1 - b_list[j]])
                    else:
                        p = None
                        break
            if p == None:
                TotalProbability[i] = 0
                continue
            TotalProbability[i] = 2 ** p
        return TotalProbability