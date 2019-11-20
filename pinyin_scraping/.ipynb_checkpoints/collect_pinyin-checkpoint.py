# coding: UTF-8
import urllib.request, urllib.error, urllib.parse
import re
from bs4 import BeautifulSoup

START=0
END=10
n=0
base_url="https://zh.wiktionary.org/wiki/"
text=""
NO_PINYINS = "NO PINYINS"

class Info():
    def __init__(self, line):
        self.line =line.replace("\n","\t")
        self.kantaiji=line.split("\t")[0]
        self.hantaiji=line.split("\t")[1]
        self.pinins=[]
    def get_kantaiji(self,):
        return self.kantaiji
    def get_hantaiji(self,):
        return self.hantaiji
    def get_output(self,soup):
        pinyins=self._get_pinyins(soup)
        if pinyins[0] == "ERROR" or pinyins[0] == "NOT FOUND":
            return NO_PINYINS
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
    
def get_result (character):
    html = urllib.request.urlopen(url=base_url+urllib.parse.quote(character))
    soup = BeautifulSoup(html, "html.parser")
    return info.get_output(soup)
    

with open("./kantaiji_list.txt", mode='r', encoding="utf-8_sig") as f:
    lines=f.readlines()
    # lines=lines[START:END]
    for line in lines:
        n+=1
        # if n>=END:
        #     break
        info=Info(line)
        output_line=get_result(info.get_kantaiji())
        if output_line == NO_PINYINS:
            output_line=get_result(info.get_hantaiji())
        print(str(n))
        print(output_line)
        text+=output_line


with open("./pinyin_list_hantaiji.txt", mode='w', encoding="utf-8_sig") as f:
    f.write(text)
