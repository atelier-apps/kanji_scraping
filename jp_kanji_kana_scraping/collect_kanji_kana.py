# coding: UTF-8
import urllib.request, urllib.error, urllib.parse
import itertools
import re
from bs4 import BeautifulSoup

#バグ発見のための弁


base_url="https://ja.wiktionary.org/wiki/"
text=""
n=5 # 書き込みを始めたい行数(始めたい行より、-1行書く)
MAX=10 # 書き込みが終わる行数
check_n=5
with open("./jp_kanji_list.txt", mode='r', encoding="utf-8_sig") as f:
    #lines=f.readlines()
    for line in itertools.islice(f, n, MAX):
        check_n+=1
        # n+=1
        # if n > MAX:
        #     break
        character=line.replace("\n","")
        html = urllib.request.urlopen(url=base_url+urllib.parse.quote(character))
        soup = BeautifulSoup(html, "html.parser")
        #ここを改良する必要あり。このタグの後ろの値を取る。
        kanon_label_tag = soup.find("a", {"title":"漢音"})
        if kanon_label_tag==None:
            text+="KANON NOT FOUND\n"
            print(str(n)+": "+character+": KANON NOT FOUND")
            continue
        #ここで漢音タグの後ろの値を取っているのか
        kanon_tag=kanon_label_tag.parent.find("a",{"title":re.compile("^[ァ-ヶ]+$")})
        text+=kanon_tag["title"]+"\n"
        print(str(check_n)+": "+character+": "+kanon_tag["title"])



with open("./" + str(n) + "-" + str(MAX) + "kanji_kana_list.txt", mode='w') as f: # 行数ごとにファイルを作成し、書き込みを行う
    f.write(text)
