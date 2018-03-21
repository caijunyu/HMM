# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 21:16:59 2018

@author: robocai
"""

import math

infinite = float(-2**31)

#对a矩阵每一行归一化，a矩阵都*log
def log_normalize(a):
    s = 0
    for x in a:
        s += x
    if s == 0:
        print "Error..from log_normalize."
        return
    s = math.log(s)
    
    for i in range(len(a)):
        if a[i] == 0:
            a[i] = infinite
        else:
            a[i] = math.log(a[i]) - s
    

#状态序列：B,M,E,S
#观测序列：65536
def mle():
    #pi\A\B初始化
    pi = [0] * 4 # npi[i]：i状态的个数
    A = [[0] * 4 for x in range(4)]       # na[i][j]：从i状态到j状态的转移个数
    B = [[0]* 65536 for x in range(4)]   # nb[i][o]：从i状态到o字符的个数
    
    #读入数据
    f = file(".\\24.pku_training.utf8")
    data = f.read()[3:].decode('utf-8')
    f.close
    tokens = data.split('  ')
    
    last_q = 2 #随机初始状态
    old_progress = 0
    print '进度：'

    for k, token in enumerate(tokens):
        process = float(k) / float(len(tokens))
        if process > old_progress + 0.1:
            old_progress = process
            print('%.3f' % process)
            
        token = token.strip()
        n = len(token)
        
        if n <= 0:
            continue
        if n == 1: #单字
            pi[3] += 1
            A[last_q][3] += 1
            B[3][ord(token[0])] += 1
            last_q = 3
            continue
        #如果词》=2个字，则以下：
        # 初始向量
        pi[0] += 1
        pi[2] += 1
        pi[1] += n-2
        # 转移矩阵
        A[last_q][0] += 1
        last_q = 2
        if n == 2:
            A[0][2] += 1
        else: 
            A[0][1] += 1
            A[1][1] += n-3
            A[1][2] += 1
        # 发射矩阵
        B[0][ord(token[0])] += 1
        B[2][ord(token[n-1])] += 1
        for i in range(1, n-1):
            B[1][ord(token[i])] += 1
        
    # 正则化
    log_normalize(pi)
    for i in range(4):
        log_normalize(A[i])
        log_normalize(B[i])
    return [pi, A, B]
        

def list_write(f, v):
    for a in v:
        f.write(str(a))
        f.write(' ')
    f.write('\n')

def save_parameter(pi, A, B):
    f_pi = open(".\\pi.txt", "w")
    list_write(f_pi, pi)
    f_pi.close()
    f_A = open(".\\A.txt", "w")
    for a in A:
        list_write(f_A, a)
    f_A.close()
    f_B = open(".\\B.txt", "w")
    for b in B:
        list_write(f_B, b)
    f_B.close()



if __name__ == "__main__":
    pi, A, B = mle()
    save_parameter(pi, A, B)
    print "训练完成..."
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        