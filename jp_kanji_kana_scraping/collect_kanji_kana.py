# coding: UTF-8
import urllib.request, urllib.error, urllib.parse
import itertools
import re
from bs4 import BeautifulSoup

base_url="https://ja.wiktionary.org/wiki/"
text=""
n=0 # 書き込みを始めたい行数(始めたい行より、-1行書く)
check_n=0 #nと同じ値になる
MAX=250 # 書き込みが終わる行数

with open("./jp_kanji_list.txt", mode='r', encoding="utf-8_sig") as f:
    #lines=f.readlines()
    for line in itertools.islice(f, n, MAX):
        check_n+=1
        character=line.replace("\n","")
        #URLを叩いてページが見つからなかったときのエラーをはじく
        try:
            html = urllib.request.urlopen(url=base_url+urllib.parse.quote(character))
            soup = BeautifulSoup(html, "html.parser")
        except:
            print(str(check_n)+": "+character+": WIKI DOESN'T HAVE THIS PAGE")
            continue
        #カナを検索
        kanon_label_tag = soup.find("a", {"title":"漢音"})
        if kanon_label_tag==None:
            text+="KANON NOT FOUND\n"
            print(str(n)+": "+character+": KANON NOT FOUND")
            continue
        #ここでNonetypeのエラーをはじく
        try:
            kanon_tag=kanon_label_tag.parent.find("a",{"title":re.compile("^[ァ-ヶ]+$")})
            text+=kanon_tag["title"]+"\n"
            print(str(check_n)+": "+character+": "+kanon_tag["title"])
        except:
            print(str(check_n)+": "+character+": Skip Nonetype ERROR")
            continue


with open("./" + str(n) + "-" + str(MAX) + "kanji_kana_list.txt", mode='w') as f: # 行数ごとにファイルを作成し、書き込みを行う
    f.write(text)
