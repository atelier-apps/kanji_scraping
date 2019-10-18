# coding: UTF-8
import urllib.request, urllib.error, urllib.parse
import re
from bs4 import BeautifulSoup

START=2500
END=2563
n=0
base_url="https://ja.wiktionary.org/wiki/"
text=""
with open("./traditional_hanzi_list_full.txt", mode='r') as f:
    lines=f.readlines()
    lines=lines[START:END]
    for line in lines:
        print(START+n)
        n+=1
        character=line.replace("\n","")
        try:
            html = urllib.request.urlopen(url=base_url+urllib.parse.quote(character))
        except:
            output=character+"\t"+character+"\n"
            text+=output
            print("NOT FOUND\n"+output)
            continue
        soup = BeautifulSoup(html, "html.parser")
        kanji_label_tag = soup.find(string=re.compile("新字体"))
        if kanji_label_tag==None:
            output=character+"\t"+character+"\n"
            text+=output
            continue
        kanji_tags=None
        tag=kanji_label_tag
        while True:
            tag=tag.previous
            if tag.name=="span":
                kanji_tags=tag.find_all("a")
                break
        for kanji_tag in kanji_tags:
            kanji=kanji_tag.text
            output=character+"\t"+kanji+"\n"
            text+=output


with open("./kanji_list.txt", mode='w') as f:
    f.write(text)
