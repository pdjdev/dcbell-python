#크롤링이 잘 되는지 테스트하는 용도입니다.
#아스키 테이블로 출력됩니다.

from bs4 import BeautifulSoup
from urllib.request import urlopen
from prettytable import PrettyTable
import requests

gallid = "euca" #갤러리 ID 입력

print ("========DCBELL 설정 값========")
print ("갤러리ID: " + gallid)
print ("업데이트 간격: " + str(updTime) + "초")
print ("==============================")
print("요청시작...")

html = urlopen('https://gall.dcinside.com/mgallery/board/lists?id=' + gallid).read()
soup = BeautifulSoup(html, "html.parser")
link = soup.find_all("tr", { "class" : "ub-content us-post"})

print ("=========글 출력 시작=========")

tb = PrettyTable(['Num', 'Title', 'Name(IP)'])
tb.align = 'l'

for m in link:

  #게시글 제목
  tmp = m.find("td", { "class" : "gall_tit ub-word"})
 
  if "<b>" not in str(tmp):
    title = tmp.a.text
      
    #게시글 번호
    postnum = m.find("td", { "class" : "gall_num"}).text

    #게시글 작성자 (유동은 IP)
    tmp = m.find("td", { "class" : "gall_writer ub-writer"})
    name = tmp.find("em").text
    ip = tmp.find("span", { "class" : "ip"})

    if ip is not None:
      ip = ip.text
    else:
      ip = "고닉"

    tb.add_row([postnum, title, name + " (" + ip + ")" ])


print (tb)
print ("===========작업 끝============")
