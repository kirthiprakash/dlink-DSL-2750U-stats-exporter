# import requests
# 
# cookies = {
#     # 'sessionid': '5d5a2e52',
#     'language': 'en_us',
#     'sys_UserName': 'admin',
# }
# 
# headers = {
#     'Connection': 'keep-alive',
#     'Pragma': 'no-cache',
#     'Cache-Control': 'no-cache',
#     'Origin': 'http://192.168.100.2',
#     'Upgrade-Insecure-Requests': '1',
#     'Content-Type': 'application/x-www-form-urlencoded',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'Referer': 'http://192.168.100.2/cgi-bin/webproc',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
# }
# 
# data = {
#   'getpage': 'html/index.html',
#   'errorpage': 'html/main.html',
#   'var:menu': 'setup',
#   'var:page': 'wizard',
#   'obj-action': 'auth',
#   ':username': 'admin',
#   ':password': 'admin',
#   ':action': 'login',
#   #':sessionid': '5d5a2e52'
# }
# 
# try:
#     login_resp = requests.post('http://192.168.100.2/cgi-bin/webproc', headers=headers, cookies=cookies, data=data, verify=False)
# except Exception as e:
#     print(e)
# print(login_resp.headers)
# print(login_resp.status_code)
import re
import urllib.request
from urllib.error import HTTPError
import requests
import time

def init():
    cookies = {
        'sessionid': '22be55bf',
        'language': 'en_us',
        'sys_UserName': 'admin',
    }

    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Origin': 'http://192.168.100.2',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://192.168.100.2/cgi-bin/webproc',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    data = {
      'getpage': 'html/index.html',
      'errorpage': 'html/main.html',
      'var:menu': 'setup',
      'var:page': 'wizard',
      'obj-action': 'auth',
      ':username': 'admin',
      ':password': 'admin',
      ':action': 'login',
      ':sessionid': '22be55bf'
    }
    response = requests.post('http://192.168.100.2/cgi-bin/webproc', headers=headers, cookies=cookies, data=data, verify=False)


def Scrape():
    init()
    bytes_sent = 0
    bytes_received = 0
    init_response = urllib.request.urlopen('http://192.168.100.2/cgi-bin/webproc')
    cookie = init_response.headers.get('set-cookie')
    match = re.match(r'sessionid=(.*); e', cookie)
    session_id = ''
    if match:
        session_id = match.groups()[0].strip()
    try:
        session_id = "22be55bf" # session from browser. It doens't seem to change so reusing it here. The normal flow of acquiring a new sesion id is not working
        req = urllib.request.Request('http://192.168.100.2/cgi-bin/webproc', data=b'getpage=html%2Findex.html&errorpage=html%2Fmain.html&var%3Amenu=status&var%3Apage=statistics&obj-action=auth&%3Ausername=admin&%3Apassword=admin&%3Aaction=login')
        req.add_header('Cookie', 'sessionid={}; language=en_us; sys_UserName=admin'.format(session_id))
        req.add_header('Referer', 'http://192.168.100.2/cgi-bin/webproc')
        req.add_header('Host', '192.168.100.2')
        req.add_header('Connection', 'keep-alive')
        req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')
        req.add_header('Upgrade-Insecure-Requests', '1')
        req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36')
        req.add_header('Cache-Control', 'no-cache')
        req.add_header('Accept-Language', 'en-GB,en-US;q=0.9,en;q=0.8')
        req.add_header('Accept-Encoding',  'gzip, deflate')
        urllib.request.urlopen(req)
    except HTTPError as httpError:
        if httpError.status == 302:
            # time.sleep(5)
            headers = httpError.headers.get_payload()
            match = re.search('sessionid=(.*)', headers)
            if match:
                two_session = match.groups()[0]
                two_session = two_session.strip()

                print("----{}-{}--".format(session_id, two_session))

                match = re.search('Location:(.*)', headers)
                location = ""
                if match:
                    location = match.groups()[0]
                    location = location.strip()
                    
                req = urllib.request.Request('http://192.168.100.2{}'.format(location))
                req.add_header('Cookie', 'sessionid={}; language=en_us; sys_UserName=admin'.format(session_id))
                # req.add_header('Cookie', 'sessionid={}; language=en_us; sys_UserName=admin'.format("22be55bf"))
                req.add_header('Referer', 'http://192.168.100.2/cgi-bin/webproc')
                req.add_header('Host', '192.168.100.2')
                req.add_header('Connection', 'keep-alive')
                req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')
                req.add_header('Upgrade-Insecure-Requests', '1')
                req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36')
                req.add_header('Cache-Control', 'no-cache')
                req.add_header('Accept-Language', 'en-GB,en-US;q=0.9,en;q=0.8')
                req.add_header('Accept-Encoding',  'gzip, deflate')
                response = urllib.request.urlopen(req)
                print(response.url)
                content_b = response.readlines()
                match = re.search(r'G_LanStatus\[m\]\[1\]\ =\ "(.*?)";', str(content_b))
                if match:
                    bytes_sent = int(match.groups()[0].strip())
                match = re.search(r'G_LanStatus\[m\]\[2\]\ =\ "(.*?)";', str(content_b))
                if match:
                    bytes_received = int(match.groups()[0].strip())

                print(bytes_sent, bytes_received)

    return bytes_sent, bytes_received
