# coding: UTF-8
import urllib.request, urllib.error, urllib.parse
import re
from bs4 import BeautifulSoup

START=0
END=10
n=0
base_url="https://zh.wiktionary.org/wiki/"
text=""

class Info():
    def __init__(self, line):
        self.line =line.replace("\n","\t")
        self.character=line.split("\t")[0]
        self.pinins=[]
    def get_character(self,):
        return self.character
    def get_output(self,soup):
        pinyins=self._get_pinyins(soup)
        output=[]
        for pinyin in pinyins:
            output.append(self.line+pinyin+"\t"+str(len(pinyins))+"\n")
        return "".join(output)
    def _check_pinyin_tag(self,soup):
        self.tag = soup.find("a", text=re.compile("^拼音$"))
        if self.tag!=None:
            self.mode=1
            return
        self.tag = soup.find("a", text=re.compile("^(汉语拼音|漢語拼音)$"))
        if self.tag!=None:
            if self.tag.parent.name=="li":
                self.mode=2
            elif self.tag.parent.name=="b":
                self.mode=3
            return
        self.tag=soup.find("b", text=re.compile("^(现代北京音（汉语拼音）|現代北京音（漢語拼音）)$"))
        if self.tag!=None:
            self.mode=4
            return
        self.mode=-1
    def _get_pinyins(self,soup):
        self._check_pinyin_tag(soup)
        try:
            if self.mode==1 or self.mode==3:
                pinyins=self.tag.parent.parent.parent.find_all(text=re.compile("^.*[āáǎàēéěèīíǐìōóǒòūúǔùüǖǘǚǜ].*$"))
                return pinyins
            elif self.mode==2:
                pinyin_text=self.tag.parent.find(text=re.compile("^.*[āáǎàēéěèīíǐìōóǒòūúǔùüǖǘǚǜ].*$"))
                pinyins=pinyin_text.replace(" ","").replace("：","").replace(":","").replace("*","").split(",")
                return pinyins
            elif self.mode==4:
                pinyins=self.tag.parent.parent.parent.parent.find_all(text=re.compile("^.*[āáǎàēéěèīíǐìōóǒòūúǔùüǖǘǚǜ].*$"))
                return pinyins
        except:
            return ["ERROR"]
        return ["NOT FOUND"]


with open("./kantaiji_list.txt", mode='r') as f:
    lines=f.readlines()
    lines=lines[START:END]
    for line in lines:
        n+=1
        if n>=END:
            break
        info=Info(line)
        html = urllib.request.urlopen(url=base_url+urllib.parse.quote(info.get_character()))
        soup = BeautifulSoup(html, "html.parser")
        output_line=info.get_output(soup)
        print(str(n))
        print(output_line)
        text+=output_line


with open("./pinyin_list.txt", mode='w') as f:
    f.write(text)
