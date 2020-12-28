# -*- encoding: utf-8 -*-
"""
@author : youngbai
@time : 2020/12/27 21:33
@file : RefD-EQUAL.py
@desc :
"""
import pandas as pd
from mediawiki import MediaWiki
wikipedia = MediaWiki()

def read_Data(url):
    '''
    读取Excel的数据，返回A、B列的概念
    I：
    -----
    url：文件地址
    O：
    -----
    g：A列概念
    h：B列概念
    '''
    df = pd.read_excel(url)
    g = df['A'].tolist()
    h = df['B'].tolist()
    return g,h


def RefD_left(A, B):
    '''
        计算RefD公式的左半部分
    输入：
    ——————
    A：A概念
    B：B概念
    输出：
    ——————
    sum_l：左半边的值

    '''
    p = wikipedia.page(A)
    w_ci_A_list =p.backlinks   # weights the importance of ci to A;
    fm = len(w_ci_A_list)
    fz = 0
    for element in w_ci_A_list:
        # 寻找R(ci,A)中的frontlinks
        try:
            p1 = wikipedia.page(element,auto_suggest=False)
        except:
            topics = wikipedia.search(element)
            print(str(i) + " may refer to: ")
            for i, topic in enumerate(topics):
                print(i, topic)
            choice = int(input("Enter a choice: "))
            assert choice in range(len(topics))
            p1 = wikipedia.page(topics[choice])
        A_outlinks_list = p1.links
        A_outlinks_set = set(A_outlinks_list)
        if(B in A_outlinks_set):
            fz += 1

    sum_l = fz/fm
    print(sum_l)
    return sum_l


def RefD_right(A, B):
    '''
        计算RefD公式的左半部分
    输入：
    ——————
    A：A概念
    B：B概念
    输出：
    ——————
    sum_r：右半边半边的值
    '''

    p = wikipedia.page(B)
    w_ci_B_list = p.backlinks  # weights the importance of ci to B;
    fm = len(w_ci_B_list)
    fz = 0
    for element in w_ci_B_list:
        # 寻找R(ci,A)中的frontlinks
        try:
            p1 = wikipedia.page(element,auto_suggest=False)
        except:
            topics = wikipedia.search(element)
            print(str(i) + " may refer to: ")
            for i, topic in enumerate(topics):
                print(i, topic)
            choice = int(input("Enter a choice: "))
            assert choice in range(len(topics))
            p1 = wikipedia.page(topics[choice])
        B_outlinks_list = p1.links   # w(ci to B) and ci's links
        B_outlinks_set = set(B_outlinks_list)
        if (A in B_outlinks_set):  # whether ci's links include A
            fz += 1

    sum_r = fz / fm
    print(sum_r)
    return sum_r

if __name__ == '__main__':
    url1 = 'F:/Paper/2015-measuring_prerequisite_relations_among_concepts/Data/data_mining.xlsx'
    g,h = read_Data(url1)
    for i, j in enumerate(h):
        A = g[i]  # A概念
        B = j  # B概念
    # A = 'DBSCAN'
    # B = 'Arithmetic mean'
        sum_l = RefD_left(A, B)
        sum_r = RefD_right(A, B)
        print(sum_l-sum_r)

    # B = 'DBSCAN'
    # A = 'Arithmetic mean'
    # sum_l = RefD_left(A, B)
    # sum_r = RefD_right(A, B)
    # print(sum_l - sum_r)