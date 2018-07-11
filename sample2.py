import os
import re
import numpy as np
from numpy.random import *
import hashlib
import tkinter as tk


# 単語を格納するための空のリスト（単語リスト）を作成
pre_words = []
words = []


# テキストファイルかどうかをチェックする機能の実装。
# 対象となるファイルが .txt ならTrue、それ以外なら Falseを返す。
def text_checker(name):
    text_regex = re.compile(r'.+\.txt')
    if text_regex.search(str(name)):
        return True
    else:
        return False


# テキストファイルの文字列を単語に分割してリスト化する機能の実装。
def word_list(text):
    f = open(text)
    data = f.read()
    # 空白文字列で区切る。
    for word in data.split():
        word_1=word.replace(".","")
        word_2=word_1.replace(",","")
        pre_words.append(word_2)


# wordsに単語を格納していく機能の実装。
# 対象フォルダのファイルを順番に開いていき、txtファイルの判定→単語リストの格納を実行する。
# txtファイル以外は pass する。

for file in os.listdir(os.getcwd()):
    if text_checker(file):
        word_list(file)
    else:
        pass

for lw in pre_words:
    lower_word = lw.lower()
    words.append(lower_word)

# 単語リストに格納されたデータから、各単語の使用回数を計算し、使用回数の多い順にならべかえる。

# 単語の使用頻度を取りまとめる空の辞書を作成。
# キーが単語、値が回数
word_counter = {}

#for w in words:
    #word_counter.setdefault(w, 0)
    #word_counter[w] = word_counter[w] + 1
D=[]
for w in words:
    if w not in D:
        D.append(w)
#print(len(D))

directIndex=[[],[]]
counter=-1
for file in os.listdir(os.getcwd()):
    if text_checker(file):
        counter=counter+1
        pre_words = []
        word_list(file)
        for lw in pre_words:
            lower_word = lw.lower()
            hash_word=hashlib.sha256(lower_word.encode('utf-8')).hexdigest()
            hash_word_10=int(hash_word,16)
            if hash_word_10%10000 not in directIndex[counter]:
                directIndex[counter].append(hash_word_10%10000)
    else:
        pass
D1=directIndex[0]
D2=directIndex[1]
#print(D1[1])
#print(directIndex)

A=len(D1)
#print(A)

Ind1=np.zeros(100)
Ind2=np.zeros(100)

s=57
def tp(sk,keyword):
    q=(sk*sk+keyword)%100
    return q

prg=[]
seed(s)
prg=randint(0,2,100)
#print(prg)

for i in range(len(D1)):
    q=tp(s,D1[i])
    Ind1[q]=1
    i=i+1

for i in range(len(D2)):
    q=tp(s,D2[i])
    Ind2[q]=1
    i=i+1

for i in range(len(Ind1)):
    pr=int(prg[i])
    I1=int(Ind1[i])
    I2=int(Ind2[i])
    Ind1[i]=int((I1+pr)%2)
    Ind2[i]=int((I2+pr)%2)
#print(Ind1)

#print(Ind2)

def st(s,keyword):
    lr = keyword.lower()
    hash_word_s = hashlib.sha256(lr.encode('utf-8')).hexdigest()
    hash_word_st = int(hash_word_s, 16)
    hash_word_st_1 = hash_word_st % 10000
    s_int = int(s)
    h_int = int(hash_word_st_1)
    q = tp(s_int, h_int)
    seed(s)
    prg = randint(0, 2, 100)
    prg_st = prg[q]
    return q,prg_st


def search(s,keyword,list):
    #lr=keyword.lower()
    #hash_word_s= hashlib.sha256(lr.encode('utf-8')).hexdigest()
    #hash_word_st = int(hash_word_s, 16)
    #hash_word_st_1=hash_word_st%10000
    #s_int=int(s)
    #print(s_int)
    #h_int=int(hash_word_st_1)
    #print(h_int)
    #q = tp(s_int,h_int)
    #print(q)
    #seed(s)
    #prg=randint(0,2,100)
    #st=prg[q]
    searchToken=st(s,keyword)
    q=int(searchToken[0])
    prg_st=int(searchToken[1])
    li=int(list[q])
    ans=int((li+prg_st)%2)
    return ans

print(D)
searchword='cryptography'
result1=search(s,searchword,Ind1)
result2=search(s,searchword,Ind2)
print(result1)
print(result2)

root = tk.Tk()
root.title(u"Sever has")
root.geometry("400x300")

label = tk.Label(root, text="Index1")
#表示
label.grid()
label_Ind1 = tk.Label(root, text=Ind1)
label_Ind1.grid()
label2 = tk.Label(root, text="Index2")
label2.grid()
label_Ind2 = tk.Label(root, text=Ind2)
label_Ind2.grid()
Ind2_print=Ind1
#label_Ind3 = tk.Label(root, text='[{0}{1}{2}]'.format(Ind2_print[0:int(st(s,searchword)[0])-1],Ind2_print[int(st(s,searchword)[0])],Ind2[int(st(s,searchword)[0]+1):len(Ind2)]))
#label_Ind3.grid()



root_1 = tk.Tk()
root_1.title(u"Sever searches")
root_1.geometry("400x300")
#label_1 = tk.Label(root_1, text="Server receives")
label_2 = tk.Label(root_1, text='server receives search token:')
label_3 = tk.Label(root_1, text='st={0}, prn={1}'.format(st(s,searchword)[0],st(s,searchword)[1]))
label_empty=tk.Label(root_1, text='')
label_search=tk.Label(root_1, text='search execution')
label_4 = tk.Label(root_1, text='Index1[{0}] XOR prn={1} XOR {2}={3}'.format(int(st(s,searchword)[0]),int(Ind1[st(s,searchword)[0]]),st(s,searchword)[1],search(s,searchword,Ind1)))
label_5 = tk.Label(root_1, text='Index2[{0}] XOR prn={1} XOR {2}={3}'.format(int(st(s,searchword)[0]),int(Ind2[st(s,searchword)[0]]),st(s,searchword)[1],search(s,searchword,Ind2)))


#表示
#label_1.grid()
label_2.grid()
label_3.grid()
label_empty.grid()
label_search.grid()
label_4.grid()
label_5.grid()


root.mainloop()
root_1.mainloop()