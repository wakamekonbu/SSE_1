import os
import re
import numpy as np
from numpy.random import *
import hashlib
import tkinter as tk

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
        word = word.lower() # 大文字 -> 小文字へ
        word = word.replace(".","") # ピリオドを消去
        word = word.replace(",","") # カンマを消去
        words.append(word) # wordsにwordを追加する

def tp(sk, keyword):
    q = (sk*sk + keyword) % 100
    return q

# txtファイルに存在する単語を格納する空のリスト（単語リスト）を作成
words = [] # 単語の重複あり
D = [] # 単語の重複なし　dictionary の D らしい

directIndex = [[] for i in range(2)] #[[], []]と同じ
counter = -1
# カレントディレクトリ(os.getcwd())にあるファイルを取得する(os.listdir)
for file in os.listdir(os.getcwd()):
    # txtファイルのみを取り出す
    if text_checker(file):
        counter = counter + 1
        word_list(file)
        for w in words:
            # sha256というハッシュ関数を用いて、単語の16進数のハッシュ値を生成
            hash_word = hashlib.sha256(w.encode('utf-8')).hexdigest()# hash_wordはstr型
            # ハッシュ値を整数に変換
            hash_word_10 = int(hash_word,16)
            # 衝突したら弾く
            if hash_word_10 % 10000 not in directIndex[counter]:
                directIndex[counter].append(hash_word_10 % 10000)
            
            # D に words 内の単語を重複しないように追加する
            if w not in D:
                D.append(w)
    else:
        pass

D1 = directIndex[0]
D2 = directIndex[1]
Ind1 = np.zeros(100) # Ind1 = [0, 0, 0, .... 0]
Ind2 = np.zeros(100) # Ind2 = [0, 0, 0, .... 0]

s = 57 # 乱数のシード
seed (s) 
prg = [] 
prg = randint(0,2,100) # [0, 2)の100個の整数の乱数を得る

print(D1)

for i in range(len(D1)):
    q = tp(s, D1[i])
    Ind1[q] = 1
    i = i + 1

for i in range(len(D2)):
    q = tp(s, D2[i])
    Ind2[q] = 1
    i= i + 1

for i in range(len(Ind1)):
    pr = int(prg[i])
    I1 = int(Ind1[i])
    I2 = int(Ind2[i])
    Ind1[i] = int((I1+pr) % 2)
    Ind2[i] = int((I2+pr) % 2)

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
    """
    lr=keyword.lower()
    hash_word_s= hashlib.sha256(lr.encode('utf-8')).hexdigest()
    hash_word_st = int(hash_word_s, 16)
    hash_word_st_1=hash_word_st%10000
    s_int=int(s)
    print(s_int)
    h_int=int(hash_word_st_1)
    print(h_int)
    q = tp(s_int,h_int)
    print(q)
    seed(s)
    prg=randint(0,2,100)
    st=prg[q]
    """
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



# GUI関連----------------------------
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
