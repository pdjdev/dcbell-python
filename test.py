from bs4 import BeautifulSoup
from urllib.request import urlopen
from prettytable import PrettyTable

gallid = input("갤러리 ID?: ")#갤러리 ID 입력

html = urlopen("https://gall.dcinside.com/board/lists?id=" + gallid).read()

print("요청시작...")

try:

  print("갤러리 종류: ", end='')
  if "location.replace" in str(html):
    print("마이너 갤러리")
    html = urlopen("https://gall.dcinside.com/mgallery/board/lists?id=" + gallid).read()
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
