from bs4 import BeautifulSoup
from prettytable import PrettyTable
import urllib.request

gallid = input("갤러리 ID?: ")#갤러리 ID 입력

hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'}

req = urllib.request.Request("https://gall.dcinside.com/board/lists?id=" + gallid, headers = hdr)
html = urllib.request.urlopen(req).read()

print("요청시작...")

try:

  print("갤러리 종류: ", end='')
  if "location.replace" in str(html):
    print("마이너 갤러리")
    req = urllib.request.Request("https://gall.dcinside.com/mgallery/board/lists?id=" + gallid, headers = hdr)
    html = urllib.request.urlopen(req).read()
  else:
    print("정식 갤러리")

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

except Exception as ex:
   print("오류 발생:", ex)


print ("===========작업 끝============")
