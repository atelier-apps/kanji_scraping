# coding: UTF-8
import urllib.request, urllib.error, urllib.parse
import re
from bs4 import BeautifulSoup

MAX=1

base_url="https://zh.wiktionary.org/wiki/"
text=""
n=0
with open("./kantaiji_list.txt", mode='r', encoding="utf-8_sig") as f:
    lines=f.readlines()
    for line in lines:
        n+=1
        if n > MAX:
            break
        character=line.replace("\n","")
        html = urllib.request.urlopen(url=base_url+urllib.parse.quote(character))
        soup = BeautifulSoup(html, "html.parser")

        #pinyin_label_tag = soup.find("a", {"class":"form-of pinyin-ts-form-of"})
        #if pinyin_label_tag==None:
        pinyin_tag = soup.find("span", {"class":"form-of pinyin-ts-form-of"})
        if pinyin_tag==None:
            text+="PINYIN NOT FOUND\n"
            print(str(n)+": "+character+": PINYIN NOT FOUND")
            continue
        #ここでピンインタグの後ろの値を取っているのか
        #ここを改良する必要あり。複数個あった場合を考える
        #pinyin_tag=pinyin_label_tag.parent.find("a",{"title":re.compile("^[a-zA-Z0-9]+$")})

#        text+=pinyin_tag["title"]+"\n"
        print(str(n)+": "+character+": "+pinyin_tag["title"])
#with open("./pinyin_list.txt", mode='w') as f:
#    f.write(text)
