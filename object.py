import os
import re
import numpy as np
from numpy.random import *
import hashlib

# テキストファイルかどうかをチェックする
# 対象となるファイルが .txt ならTrue、それ以外なら Falseを返す。
def text_checker(name):
    text_regex = re.compile(r'.+\.txt')
    if text_regex.search(str(name)):
        return True
    else:
        return False

# テキストファイルの文字列を単語に分割してリスト化する
def word_list(list,text):
    f = open(os.path.join("files",text))
    data = f.read()
    # 空白文字列で区切る。
    for word in data.split():
        word = word.lower() # 大文字 -> 小文字へ
        word = word.replace(".","") # ピリオドを消去
        word = word.replace(",","") # カンマを消去
        list.append(word) # listにwordを追加する

indlen=100
class Client:
    _s_=57
    _filenum_=0
    _prg_ = None

    def __init__(self):
        seed(self._s_)
        self._prg_=randint(0,2,100)

    def _tp_(self, keyword):
        # ハッシュ化されたkeywordから添字を得る

        q = (self._s_*self._s_ + keyword) % indlen
        return q

    def _st_(self, keyword):
        # 小文字へ
        lr = keyword.lower()
        # sha256というハッシュ関数を用いて、単語の16進数のハッシュ値を生成
        hash_word_s = hashlib.sha256(lr.encode('utf-8')).hexdigest()
        # hash_word_sをint型へ変換し、10000で割った余りを計算
        hash_word_st = int(hash_word_s, 16) % 10000 # ←tpでmod100するのでいらないのでは。
            
        # q: インデックスの添字
        q = self._tp_(hash_word_st)

        seed(self._s_)
        # prg: マスク共通鍵
        prg = randint(0, 2, indlen) # 0 or 1 の100個の整数の乱数を得る
        prg_st = prg[q]

        return q, prg_st # return (q, prg_st)　
    
    def _searchInd_(self, keyword, fileidx):
        # s 乱数のシード
        # keyword 検索文字列
        # fileidx 検索するファイルの添字（サンプルなら0か1）

        searchToken = self._st_(keyword)
        q = int(searchToken[0])
        prg_st = int(searchToken[1])
        li = int(server.search(q, fileidx))

        #マスク鍵と検索結果の排他的論理和
        ans = int((li + prg_st) % 2)
        return ans # keyword が存在すれば 1, しなければ 0 を返す
    
    def searchAll(self, keyword):
        for i in range(self._filenum_):
            print("file {}: {}".format(i, self._searchInd_(keyword, i)))
    
    def _getMask_(self, q, fileidx):
        # fileidxファイルのq番目の要素に対応するマスク(0 or 1)を返す
        return self._prg_[q]
        # これがfileidxによって異なる値にならないと，類似度が出せてしまう

    def _genIndex_(self, text):
        words=[]
        word_list(words, text)
        di=[] # text に含まれる単語のハッシュのリスト
        ind=np.zeros(indlen)
        for w in words:
            # sha256というハッシュ関数を用いて、単語の16進数のハッシュ値を生成
            hash_word = hashlib.sha256(w.encode('utf-8')).hexdigest() # hash_wordはstr型
            # ハッシュ値を整数に変換
            hash_word_10 = int(hash_word,16)
            # 衝突したら弾く（つまりその単語は検索不可能）
            if hash_word_10 % 10000 not in di:
                di.append(hash_word_10 % 10000)
        
        # マスク前のインデックス生成
        for x in di:
            q = self._tp_(x)
            ind[q] = 1

        # インデックスをマスク
        for i in range(indlen):
            pr = self._getMask_(i, self._filenum_+1)
            # 排他的論理和。
            ind[i] = int((ind[i]+pr) % 2)
        
        return ind
    
    def uploadFile(self, text):
        server.uploadIndex(self._genIndex_(text))
        self._filenum_+=1
        print("client: successfully uploaded '"+text+"'")




class Server:
    _Inds_=[] #np.zeros(indlen) for i in range(filenum)

    def search(self, q, fileidx):
        # q: trapdoor
        # fileidx: 検索するファイルの添字（サンプルなら0か1）
        return self._Inds_[fileidx][q]
    
    def uploadIndex(self, ind):
        self._Inds_.append(ind)
        

client = Client()
server = Server()

# カレントディレクトリ(os.getcwd())にあるファイルを取得する(os.listdir)
for file in os.listdir(os.path.join(os.getcwd(),"files")):
    if text_checker(file):
        client.uploadFile(file)

while True:
    keyword = input("search: ")
    if(keyword == "exit()" or keyword == "quit()"):
        exit()
    client.searchAll(keyword)