# coding: UTF-8
import urllib.request, urllib.error, urllib.parse
import re
from bs4 import BeautifulSoup

#バグ発見のための弁
MAX=10

base_url="https://ja.wiktionary.org/wiki/"
text=""
n=0
with open("./hanzi_list.txt", mode='r') as f:
    lines=f.readlines()
    for line in lines:
        n+=1
        if n > MAX:
            break
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
        print(str(n)+": "+character+": "+kanon_tag["title"])



with open("./kanji_kana_list.txt", mode='w') as f:
    f.write(text)
