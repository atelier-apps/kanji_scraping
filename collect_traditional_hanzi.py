# coding: UTF-8
import urllib.request, urllib.error, urllib.parse
import re
from bs4 import BeautifulSoup

START=2000
END=2500
n=0
base_url="https://zh.wiktionary.org/zh-hans/"
text=""
with open("./traditional_hanzi_list_full.txt", mode='r') as f:
    lines=f.readlines()
    lines=lines[START:END]
    for line in lines:
        print(START+n)
        n+=1
        character=line.replace("\n","")
        html = urllib.request.urlopen(url=base_url+urllib.parse.quote(character))
        soup = BeautifulSoup(html, "html.parser")
        kanji_label_tag = soup.find("a", {"title":"w:繁體字"})
        if kanji_label_tag==None:
            output=character+"\t"+character+"\n"
            text+=output
            continue
        note=",".join(re.findall(r"(（.+?）)",kanji_label_tag.parent.text))
        kanji_tags=kanji_label_tag.parent.find("span").find_all("a")
        for kanji_tag in kanji_tags:
            kanji=kanji_tag.text
            output=character+"\t"+kanji+"\t"+note+"\n"
            text+=output


with open("./traditional_hanzi_list.txt", mode='w') as f:
    f.write(text)
