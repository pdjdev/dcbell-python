from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import time

def sendTelegramMsg(APIKey, chatID, text):
  r = requests.get("https://api.telegram.org/bot"
                   + APIKey + "/sendMessage?chat_id="
                   + chatID + "&text="
                   + text + "&parse_mode=Markdown")
  return r


gallid = "galleryid" #갤러리 ID 입력
TelAPI = "123456789:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" #텔레그램 봇키
TelChan = "@channelid" #채널 주소
updTime = 60

prev_postnum = 0

print ("========DCBELL 설정 값========")
print ("갤러리ID: " + gallid)
print ("Telegram 채널ID: " + TelChan)
print ("업데이트 간격: " + str(updTime) + "초")
print ("==============================")

while(1):

  print("요청시작...")

  html = urlopen('https://gall.dcinside.com/mgallery/board/lists?id=' + gallid).read()
  soup = BeautifulSoup(html, "html.parser")
  link = soup.find_all("tr", { "class" : "ub-content us-post"})

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


      if (int(postnum) > int(prev_postnum)):
        print ("======새 글이 있습니다!=======")
        print ("│글번호: " + postnum)
        print ("│글제목: " + title)
        print ("|닉네임(아이피): " + name + " (" + ip + ")")
        print ("│푸시 보내는 중...")
        
        sendTelegramMsg(TelAPI, TelChan, "*" + gallid + " 갤러리 새 글*\n"
                        + title + " - " + name + "(" + ip + ")\n" + "[글 링크](https://gall.dcinside.com/"
                        + gallid + "/" + postnum + ")")
        print ("│보내기 완료")
        prev_postnum = postnum

        print ("===========작업 끝============")
        break
  
  print("대기중... (" + updTime + "초)")
  time.sleep(updTime)
