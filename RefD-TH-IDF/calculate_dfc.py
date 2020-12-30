# -*- encoding: utf-8 -*-
"""
@author : youngbai
@time : 2020/12/29 22:09
@file : calculate_dfc.py 
@desc :
"""
from collections import Counter
from mediawiki import MediaWiki
import re
wikipedia = MediaWiki()
import pandas as pd
import re

# 导入所有wikiPage的标题
all_titles = []
all_wiki_titles = set()
with open("F:/实验数据/enwiki/name_outs.txt", 'r', encoding='UTF-8') as f:
  for line in f:
    all_titles.extend(line.rstrip('\n').split(' '))
  for i in all_titles:
    all_wiki_titles.add(i.replace('_', ' '))  # 所有的维基百科标题去除下划线
print('导入完成')

# 读入TF-IDF-dfc

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

def getContent(A):
    countConcept_dict ={}
    # p = body(A)
    # s = str(p)
    # print(s)
    # s1 = s.replace("[[", "title")
    # s2 =s1.replace("]]", "title")
    try:
        p = wikipedia.page(A)
    except :
        p = wikipedia.page('Coproduct')
    s = str(p.html)
    concept_list = re.findall(r'title="(.*?)">',s)
    newconcept_list = []
    for i in concept_list:
        if( i in all_wiki_titles):
            print(i)
            newconcept_list.append(i)
    #newconcept_list = [x[1:-1] for x in concept_list]  # 删除“ ”
    conceptNumbers_dict = dict(Counter(newconcept_list))
    print(conceptNumbers_dict)
    return str(conceptNumbers_dict)

if __name__ == '__main__':
    url1 = 'F:/Paper/2015-measuring_prerequisite_relations_among_concepts/Data/precalculus.xlsx'
    g,h = read_Data(url1)
    C_set =set()
    for i, j in enumerate(h):
        A = g[i]  # A概念
        B = j  # B概念
        C_set.add(A)
        C_set.add(B)
    dfc_dict = {}
    for s in C_set:
        dfc_dict[s] = getContent(s)  # 获取

    dfAll = pd.DataFrame(list(dfc_dict.items()), columns=['Concepts', 'Links_Numbers'])
    dfAll.to_excel('F:/Paper/2015-measuring_prerequisite_relations_among_concepts/Data/TF-IDF-dfc/precalculus_df.xlsx')