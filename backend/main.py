import requests
from html.parser import HTMLParser
from html.entities import name2codepoint
import re
from utils import ArticleParser

pattern = re.compile(r"<li>(.*?)<\/li>")
pattern_1 = re.compile(r".*\d+年\d+月\d+日\d+时.*肺炎疫情.*")

pattern_content = re.compile(r"(?s)<!--文章start-->(.*)<!--文章end-->")
pattern_data = re.compile(r"[，、]([\u4E00-\u9FA5]{2,3})(\d+)例")

class MyHTMLParser(HTMLParser):
    results = []

    def handle_starttag(self, tag, attrs):
        print("Start tag:", tag)
        res = {}
        for attr in attrs:
            print("     attr:", attr)
            res[attr[0]]=attr[1]
        if 'title' in res.keys():
            self.results.append(res)

    def handle_endtag(self, tag):
        print("End tag  :", tag)

    def handle_data(self, data):
        print("Data     :", data)

    def handle_comment(self, data):
        print("Comment  :", data)

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        print("Named ent:", c)

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        print("Num ent  :", c)

    def handle_decl(self, data):
        print("Decl     :", data)


if __name__ == "__main__":
    r = requests.get("http://wsjkw.gd.gov.cn/zwyw_yqxx/content/post_2880075.html")
    with open('guangdong_content_sample.html','w') as f:
        f.write(r.text)
    # p = ArticleParser()
    # for m in pattern.finditer(r.text):
    #     p.feed(m.groups()[0])
    #     print('---------------')
    # # print(p.results)
    # # p.results[0]["title"]
    # newl = ""
    # for res in p.results:
    #     if pattern_1.match(res["title"]) is not None:
    #         newl = res["href"]
    #         break

    # r2 = requests.get(newl)
    # # with open('guangdong_list_sample.html','w') as f:
    # #     f.write(r2.text)
    # m = pattern_content.search(r2.text)
    # # print(m)
    # # print(m.groups()[0])
    # content = m.groups()[0]
    # for i in pattern_data.finditer(content[content.find("累计"):]):
    #     print(i.groups())
    

