# coding: UTF-8
import urllib.request, urllib.error, urllib.parse
import re
from bs4 import BeautifulSoup

base_url="https://zh.wikisource.org/zh-hans/%E7%AE%80%E5%8C%96%E5%AD%97%E6%80%BB%E8%A1%A8"
html = urllib.request.urlopen(url=base_url)
soup = BeautifulSoup(html, "html.parser")
text=""
n=0;
with open("./hanzi_list.txt", mode='r') as f:
    lines=f.readlines()
    max_n=len(lines)
    print(max_n)
    for line in lines:
        character=line.replace("\n","")
        kanji_label_tag =soup.find("td", text=re.compile(character))
        if kanji_label_tag==None:
            text+=character+"\t"+character+"\n"
            continue
        r=character+"〔(.)、*(.)*〕"
        tr_characters_array=re.findall(r,kanji_label_tag.string)
        if len(tr_characters_array)==0:
            continue
        tr_characters=tr_characters_array[0]
        for tr_character in tr_characters:
            if tr_character=="":
                continue
            text+=character+"\t"+tr_character+"\n"
        n+=1
        print(n)
        if n==30:
            break


with open("./traditional_hanzi_list.txt", mode='w') as f:
    f.write(text)
