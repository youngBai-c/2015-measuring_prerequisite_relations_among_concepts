# -*- encoding: utf-8 -*-
"""
@author : youngbai
@time : 2020/12/27 21:33
@file : RefD-EQUAL.py
@desc :
"""
import pandas as pd
from mediawiki import MediaWiki
import json
wikipedia = MediaWiki()

with open('F:/Paper/2015-measuring_prerequisite_relations_among_concepts/Data/EQUAL_backlinks/geometry.json', 'r') as f:
  backlinks_dict = json.load(fp=f)

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

# 避免重复计算的字典
allConcept_links_dict = {}

def RefD_left(A, B):
    '''
        计算RefD公式的左半部分
    输入：
    ——————
    A：A概念
    B：B概念
    输出：
    ——————
    sum_l：RefD左半部分的值

    '''
    #p = wikipedia.page(A)
    w_ci_A_list = eval(backlinks_dict[A])  # weights the importance of ci to A;
    fm = len(w_ci_A_list)
    fz = 0
    for element in w_ci_A_list:
        if(element in allConcept_links_dict.keys()):
            A_outlinks_list = eval(allConcept_links_dict[element])
            A_outlinks_set = set(A_outlinks_list)
            if (B in A_outlinks_set):
                fz += 1
        else:
            # 寻找R(ci,A)中的outlinks
            try:
                p1 = wikipedia.page(element)
            except:
                p1 = wikipedia.page('China')
            A_outlinks_list = p1.links
            allConcept_links_dict[element] = str(A_outlinks_list)
            A_outlinks_set = set(A_outlinks_list)
            if (B in A_outlinks_set):
                fz += 1

    if (fm == 0):
        return 0
    else:
        return fz / fm


def RefD_right(A, B):
    '''
        计算RefD公式的右半部分
    输入：
    ——————
    A：A概念
    B：B概念
    输出：
    ——————
    sum_r：RefD右半部分的值
    '''

    #p = wikipedia.page(B)
    w_ci_B_list = eval(backlinks_dict[B])  # weights the importance of ci to B;
    fm = len(w_ci_B_list)
    fz = 0
    for element in w_ci_B_list:
        if (element in allConcept_links_dict.keys()):
            B_outlinks_list = eval(allConcept_links_dict[element])
            B_outlinks_set = set(B_outlinks_list)
            if (A in B_outlinks_set):
                fz += 1
        else:
            # 寻找R(ci,A)中的outlinks
            try:
                p1 = wikipedia.page(element)
            except:
                p1 = wikipedia.page('China')
            B_outlinks_list = p1.links
            allConcept_links_dict[element] = str(B_outlinks_list)  #backlinks_element的links
            B_outlinks_set = set(B_outlinks_list)
            if (A in B_outlinks_set):
                fz += 1

    if (fm == 0):
        return 0
    else:
        return fz / fm

if __name__ == '__main__':
    url1 = 'F:/Paper/2015-measuring_prerequisite_relations_among_concepts/Data/geometry.xlsx'
    g,h = read_Data(url1)
    count = 0
    for i, j in enumerate(h):
        A = g[i]  # A学习资源顺序
        B = j  # B概念

        count += 1
        sum_l = RefD_left(A, B)
        sum_r = RefD_right(A, B)
        print(count,sum_l-sum_r)
