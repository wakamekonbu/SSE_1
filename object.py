import os
import re
import numpy as np
from numpy.random import *
import hashlib


indlen = 1000


# テキストファイルかどうかをチェックする
# 対象となるファイルが .txt ならTrue、それ以外なら Falseを返す。
def text_checker(name):
    text_regex = re.compile(r'.+\.txt')
    if text_regex.search(str(name)):
        return True
    else:
        return False


# テキストファイルの文字列を単語に分割してリスト化する
def word_list(list, text):
    f = open(os.path.join("files", text))
    data = f.read()
    # 空白文字列で区切る。
    for word in data.split():
        word = word.lower()  # 大文字 -> 小文字へ
        word = word.replace(".", "")  # ピリオドを消去
        word = word.replace(",", "")  # カンマを消去
        list.append(word)  # listにwordを追加する


class Client:
    _s_ = 57
    _filenum_ = 0
    _prg_ = None
    unq_prg = []
    _raw_Inds_ = []  # np.zeros(indlen) for i in range(filenum)

    def __init__(self):
        seed(self._s_)
        self._prg_ = randint(0, 2, indlen)

    def _fileunique_prg_(self, filename, filenum):
        # 多重配列のappendがよくわからんので一時的なやつ
        tmp = None
        # 小文字にする
        lr = filename.lower()
        # sha256でハッシュ
        hash_word = hashlib.sha256(lr.encode('utf-8')).hexdigest()
        # ハッシュ値をもとにシードを生成
        hash_seed = int(hash_word, 16) % 10000
        seed(hash_seed)
        # [filenum][それぞれの擬似乱数]を作成
        tmp = randint(0, 2, indlen)
        self.unq_prg.append(tmp)
        # ユーザー固有の疑似乱数の情報も追加
        for i in range(indlen):
        
        #デバッグ用。ファイル固有のprgを表示
        #print(self.unq_prg[filenum])
            self.unq_prg[filenum][i] = (self._prg_[i]+self.unq_prg[filenum][i]) % 2

    def _tp_(self, keyword):
        # ハッシュ化されたkeywordから添字を得る

        q = (self._s_*self._s_ + keyword) % indlen
        return q

    def _st_(self, keyword, fileidx):
        # 小文字へ
        lr = keyword.lower()
        # sha256というハッシュ関数を用いて、単語の16進数のハッシュ値を生成
        hash_word_s = hashlib.sha256(lr.encode('utf-8')).hexdigest()
        # hash_word_sをint型へ変換し、10000で割った余りを計算
        hash_word_st = int(hash_word_s, 16) % 10000  # ←tpでmod100するのでいらないのでは。

        # q: インデックスの添字
        q = self._tp_(hash_word_st)
        #デバッグ用
        #print("raw q is "+str(q))
        # prg: マスク共通鍵
        # prg = randint(0, 2, indlen) # 0 or 1 の100個の整数の乱数を得る
        prg_st = self.unq_prg[fileidx][q]
        
        #デバッグ用
        #print("prg_st is "+str(prg_st))

        return q, prg_st  # return (q, prg_st)　

    def _searchInd_(self, keyword, fileidx):
        # s 乱数のシード
        # keyword 検索文字列
        # fileidx 検索するファイルの添字（サンプルなら0か1）

        searchToken = self._st_(keyword, fileidx)
        q = int(searchToken[0])
        prg_st = int(searchToken[1])
        ans = server.search(q, fileidx, prg_st)
        return ans # keyword が存在すれば 1, しなければ 0 を返す


    def searchAll(self, keyword):
        for i in range(self._filenum_):
            res = self._searchInd_(keyword, i)
            print("{}: {}".format(res[1], res[0]))

    def _getMask_(self, q, fileidx):
        # fileidxファイルのq番目の要素に対応するマスク(0 or 1)を返す
        # これがfileidxによって異なる値にならないと，類似度が出せてしまう
        # return self._prg_[q]
        return self.unq_prg[fileidx][q]

    def _genIndex_(self, text):
        words = []
        word_list(words, text)
        di = []  # text に含まれる単語のハッシュのリスト
        ind = np.zeros(indlen)
        for w in words:
            # sha256というハッシュ関数を用いて、単語の16進数のハッシュ値を生成
            hash_word = hashlib.sha256(w.encode('utf-8')).hexdigest()  # hash_wordはstr型
            # ハッシュ値を整数に変換
            hash_word_10 = int(hash_word, 16)
            # 衝突したら弾く（つまりその単語は検索不可能）
            if hash_word_10 % 10000 not in di:
                di.append(hash_word_10 % 10000)
        # マスク前のインデックス生成
        for x in di:
            q = self._tp_(x)
            ind[q] = 1

        # インデックスをマスク
        for i in range(indlen):
            pr = self._getMask_(i, self._filenum_)  # filenumが+1されてないのは、配列の添字としてそのままつかってるから
            # 排他的論理和。
            ind[i] = int((ind[i]+pr) % 2)
        return ind


    def _genRawIndex_(self, text):
        words = []
        word_list(words, text)
        di = []  # text に含まれる単語のハッシュのリスト
        raw_ind = np.zeros(indlen)
        for w in words:
            # sha256というハッシュ関数を用いて、単語の16進数のハッシュ値を生成
            hash_word = hashlib.sha256(w.encode('utf-8')).hexdigest()  # hash_wordはstr型
            # ハッシュ値を整数に変換
            hash_word_10 = int(hash_word, 16)
            # 衝突したら弾く（つまりその単語は検索不可能）
            if hash_word_10 % 10000 not in di:
                di.append(hash_word_10 % 10000)
        # マスク前のインデックス生成
        for x in di:
            q = self._tp_(x)
            raw_ind[q] = 1

        # インデックスをマスク
        for i in range(indlen):
            pr = self._prg_[i]  # filenumが+1されてないのは、配列の添字としてそのままつかってるから
            # 排他的論理和。
            raw_ind[i] = int((raw_ind[i]+pr) % 2)
        return raw_ind

    def uploadFile(self, text):
        server.uploadFile(text, self._genIndex_(text))
        ind = self._genRawIndex_(text)
        self._raw_Inds_.append(ind)
        self._filenum_ += 1
        print("client: successfully uploaded '"+text+"'")

    def mal_get_correctSimilarity(self):
        # 文書の真の類似度を得る
        for i in range(len(self._raw_Inds_)):
            for j in range(i+1, len(self._raw_Inds_)):
                print("accurate similarity of {}.txt and {}.txt is:".format(i+1, j+1),
                      sum(t == s for (t, s) in zip(self._raw_Inds_[i], self._raw_Inds_[j])) / indlen)


class Server:
    _Inds_ = []  # np.zeros(indlen) for i in range(filenum)
    _filenames_ = []
    _maskInfo_ = []  # 悪意ある管理者が作成
    _search_result_= None #攻撃者による比較推定法用の配列
    _search_count_ = 0

    def search(self, q, fileidx, m):
        # q: trapdoor
        # fileidx: 検索するファイルの添字（サンプルなら0か1）
        # m: mask
        ans = bool(int(self._Inds_[fileidx][q]) ^ m)
        self._search_result_[fileidx].append(ans)
        self._maskInfo_[fileidx][q] = m  # 悪意ある管理者が作成

        return ans, self._filenames_[fileidx]

    def uploadFile(self, name, ind):
        self._Inds_.append(ind)
        self._filenames_.append(name)
        self._maskInfo_.append([None for _ in range(indlen)])  # 悪意ある管理者が作成

    def mal_get_mnglessSimilarity(self):
        # 悪意ある管理者が文書の類似度を得る
        for i in range(len(self._Inds_)):
            for j in range(i+1, len(self._Inds_)):
                print("similarity of {}.txt and {}.txt for malicious attacker is:".format(i+1, j+1),
                      sum(t == s for (t, s) in zip(self._Inds_[i], self._Inds_[j]))/indlen)

    def get_similarity_with_maskInfo(self):  # 悪意ある管理者が作成
        inds = self._Inds_
        # マスクが分かっていればマスクを外す
        for i in range(len(self._Inds_)):
            for j in range(indlen):
                if self._maskInfo_[i][j] is not None:
                    inds[i][j] = int(inds[i][j]) ^ self._maskInfo_[i][j]
        # 類似度の計算
        for i in range(len(self._Inds_)):
            for j in range(i+1, len(self._Inds_)):
                print("similarity of {}.txt and {}.txt for malicious attacker with maskInfo is:".format(i+1, j+1),
                      sum(t == s for (t, s) in zip(inds[i], inds[j]))/indlen)

    def mal_rslt_Similarity(self):
        coeff=1 # F_Fの重み係数
        for i in range(0,len(self._filenames_)):
          for j in range(i+1,len(self._filenames_)):
            T_T=0
            F_F=0
            for k in range(self._search_count_):
              T_T = T_T + float(self._search_result_[i][k] and self._search_result_[j][k])
              F_F = F_F +float(not (self._search_result_[i][k] or self._search_result_[j][k]))
            similarity = (T_T + F_F* coeff)/float(self._search_count_)
            print("similarity with result of "+self._filenames_[i]+" and "+self._filenames_[j]+" is : "+str(similarity))



client = Client()
server = Server()

print("------------")
# カレントディレクトリ(os.getcwd())にあるファイルを取得する(os.listdir)
for file in os.listdir(os.path.join(os.getcwd(), "files")):
    if text_checker(file):
        client._fileunique_prg_(file, client._filenum_)
        client.uploadFile(file)
print("------------")


server._search_result_=[[] for i in range(client._filenum_)]
server.mal_get_mnglessSimilarity()
print("------------")
client.mal_get_correctSimilarity()
print("------------")

while True:
    keyword = input("search: ")
    if(keyword == "exit()" or keyword == "quit()"):
        server.get_similarity_with_maskInfo()
        exit()
    client.searchAll(keyword)
    server._search_count_=server._search_count_+1
    server.mal_rslt_Similarity()
