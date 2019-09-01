# coding: UTF-8
import urllib.request, urllib.error
from bs4 import BeautifulSoup

# アクセスするURL
url = "https://zh.wiktionary.org/wiki/%E9%99%84%E5%BD%95:%E7%8E%B0%E4%BB%A3%E6%B1%89%E8%AF%AD%E5%B8%B8%E7%94%A8%E5%AD%97%E8%A1%A8"
base_url="https://zh.wiktionary.org"

html = urllib.request.urlopen(url=url)

soup = BeautifulSoup(html, "html.parser")

a_tags = soup.find_all("a", attrs = {'title' : True})
text=""
for a_tag in a_tags:
    title = a_tag["title"]
    if  title=="匕":
        break
    if len(title)!=1:
        continue
    href = a_tag["href"]
    text+=title+"\t"+base_url+href+"\n";


with open("./kanji_list.txt", mode='w') as f:
    f.write(text)
