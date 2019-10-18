# coding: UTF-8
import urllib.request, urllib.error, urllib.parse
import re
from bs4 import BeautifulSoup

START=0
END=20
n=0
base_url="https://zh.wiktionary.org/wiki/"
text=""
with open("./traditional_hanzi_list_full.txt", mode='r') as f:
    lines=f.readlines()
    lines=lines[START:END]
    for line in lines:
        print(n)
        n+=1
        character=line.replace("\n","")
        html = urllib.request.urlopen(url=base_url+urllib.parse.quote(character))
        soup = BeautifulSoup(html, "html.parser")
        kanon_label_tag = soup.find("a", {"title":"漢音"})

        if kanon_label_tag==None:
            text+="PINYIN NOT FOUND\n"
            print(character+": PINYIN NOT FOUND")
            continue
        kanon_tag=kanon_label_tag.parent.find("a",{"title":re.compile("^[ァ-ヶ]+$")})
        text+=character+"\t"+kanon_tag["title"]+"\n"



with open("./pinyin_list.txt", mode='w') as f:
    f.write(text)
