from bs4 import BeautifulSoup
import urllib.request, requests, time

# 헤더에 유저 에이전트 값 넣어야 요청이 제대로 옴
hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'}         

# 텔레그램 봇 요청
def sendTelegramMsg(APIKey, chatID, text):
  r = requests.get("https://api.telegram.org/bot"
                   + APIKey + "/sendMessage?chat_id="
                   + chatID + "&text="
                   + text + "&parse_mode=Markdown")
  return r

# ================= 사용 전 직접 설정해 주어야 하는 부분 =================

# 텔레그램 설정
TelAPI = "123456789:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" # 텔레그램 봇키
TelChan = "@channelid" # 주소

# 갤러리 설정 {'갤러리ID': 최근 글 번호}
# '최근 글 번호'는 특별한 경우가 아니면 0으로 두기
gall = {'gall1':0, 'gall2':0}
updTime = 60 # 업데이트 주기 (초)

# ========================================================================

# 시간 표시 형식
tType = "%Y-%m-%d %H-%M-%S"
print ("========DCBELL 설정 값========")
print ("Telegram 채널ID: " + TelChan)
print ("업데이트 간격: " + str(updTime) + "초")
print ("==============================")


while(1):

    print("[" + time.strftime(tType) + "] 요청 시작...")

    try:
        
        for g in gall.items():
            
            gallid = g[0] # 갤러리 ID
            prev_postnum = g[1] # 마지막 알림 게시글 번호

            print("[" + time.strftime(tType) + "] " + gallid + " 조회 시작...")

            #마이너, 정식갤러리 판별
            link = 'https://gall.dcinside.com/board/lists/?id=' + gallid
            r = requests.get(link, headers = hdr).text
            print('갤러리 형식:', end=' ')

            #마이너 갤러리일 경우
            if 'location.replace' in r: link = link.replace('board/','mgallery/board/'); print('마이너')
            else: print('정식')
                      
            req = urllib.request.Request(link, headers = hdr)
            html = urllib.request.urlopen(req).read()
            soup = BeautifulSoup(html, "html.parser")
            link = soup.find_all("tr", { "class" : "ub-content us-post"})

            for m in link:

                # 게시글 제목
                tmp = m.find("td", { "class" : "gall_tit ub-word"})

                if "<b>" not in str(tmp):
                    title = tmp.a.text                
                    postnum = m.find("td", { "class" : "gall_num"}).text # 게시글 번호   
                    tmp = m.find("td", { "class" : "gall_writer ub-writer"}) # 게시글 작성자 (유동은 IP)
                    name = tmp.find("em").text
                    ip = tmp.find("span", { "class" : "ip"})

                    if ip is not None: ip = ip.text
                    else: ip = "고닉"

                    # 아래에 원하는 조건문 넣어도됨
                    if (int(postnum) > int(prev_postnum)):
                        print ("======새 글이 있습니다!=======")
                        print ("│갤러리: " + gallid)
                        print ("│글번호: " + postnum)
                        print ("│글제목: " + title)
                        print ("│닉네임(아이피): " + name + " (" + ip + ")")
                        
                        # 처음에는 보내지않기 (재가동때 알림이 중복으로 가지 않도록)
                        if prev_postnum == 0:
                            print('│(최초 요청이므로 푸시를 보내지 않습니다)')
                        else:
                            print ("│푸시 보내는 중...")
                            sendTelegramMsg(TelAPI, TelChan, "*" + gallid + " 갤러리 새 글*\n"
                                                    + title + " - " + name + "(" + ip + ")\n" + "[글 링크](https://gall.dcinside.com/"
                                                    + gallid + "/" + postnum + ")")
                            print ("│보내기 완료")
                            
                        gall[gallid] = postnum
                        print ("===========작업 끝============")
                        break

            time.sleep(1)

    # 오류발생시 무시하고 반복 (서버가 오류가 좀 잦음)
    except Exception as ex: print("[" + time.strftime(tType) + "] 오류 발생! 무시후 다시 시도합니다.", ex)

    print("[" + time.strftime(tType) + "] 대기중... (" + str(updTime) + "초)")
    time.sleep(updTime)
