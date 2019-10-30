from bs4 import BeautifulSoup
import urllib.request, requests, time

# 텔레그램 봇 요청
def sendTelegramMsg(APIKey, chatID, text):
  r = requests.get("https://api.telegram.org/bot"
                   + APIKey + "/sendMessage?chat_id="
                   + chatID + "&text="
                   + text + "&parse_mode=Markdown")
  return r

# 텔레그램 설정
TelAPI = "123456789:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" # 텔레그램 봇키
TelChan = "@channelid" # 주소

# 갤러리 설정
gallid = "galleryid" # 갤러리 ID
updTime = 60 # 업데이트 주기 (초)

# 마지막 알림 게시글 번호
prev_postnum = 0

# 시간 표시 형식
tType = "%Y-%m-%d %H-%M-%S"

print ("========DCBELL 설정 값========")
print ("갤러리ID: " + gallid)
print ("Telegram 채널ID: " + TelChan)
print ("업데이트 간격: " + str(updTime) + "초")
print ("==============================")


while(1):

    print("[" + time.strftime(tType) + "] 요청시작...")

    try:
        # 헤더에 유저 에이전트 값 넣어야 요청이 제대로 옴
        hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'}
        req = urllib.request.Request("https://gall.dcinside.com/mgallery/board/lists?id=" + gallid, headers = hdr)
        html = urllib.request.urlopen(req).read()

        soup = BeautifulSoup(html, "html.parser")
        link = soup.find_all("tr", { "class" : "ub-content us-post"})

        for m in link:

            # 게시글 제목
            tmp = m.find("td", { "class" : "gall_tit ub-word"})

            if "<b>" not in str(tmp):
                title = tmp.a.text

                # 게시글 번호
                postnum = m.find("td", { "class" : "gall_num"}).text

                # 게시글 작성자 (유동은 IP)
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
                    print ("│닉네임(아이피): " + name + " (" + ip + ")")
                    print ("│푸시 보내는 중...")

                    sendTelegramMsg(TelAPI, TelChan, "*" + gallid + " 갤러리 새 글*\n"
                                            + title + " - " + name + "(" + ip + ")\n" + "[글 링크](https://gall.dcinside.com/"
                                            + gallid + "/" + postnum + ")")
                    print ("│보내기 완료")
                    prev_postnum = postnum

                    print ("===========작업 끝============")
                    break

    # 오류발생시 무시하고 반복 (서버가 오류가 좀 잦음)
    except Exception as ex:
        print("[" + time.strftime(tType) + "] 오류 발생! 무시후 다시 시도합니다.", ex)

    print("[" + time.strftime(tType) + "] 대기중... (" + str(updTime) + "초)")
    time.sleep(updTime)

