import logging

from config import PROXIES, USER_AGENTS

from selenium.webdriver.common.by import By


def check_if_valid_url(url):
    return 'adidas' in url and url.startswith('http://www.')


def is_past_queue_cookie(cookie):
    return ('hmac=' in cookie['value']) or ('gceeqs' == cookie['name'])


def check_if_past_queue(driver):
    for cookie in driver.get_cookies():
        is_valid = is_past_queue_cookie(cookie)
        if is_valid:
            return True
    return False


def get_proxy(index):
    proxy = None
    try:
        proxy = PROXIES[index]
    except IndexError:
        round = int(index / len(PROXIES))
        proxy = PROXIES[(index - (round * len(PROXIES)))]

    return proxy[0], proxy[1]


def get_user_agent(index):
    try:
        return USER_AGENTS[index]
    except IndexError:
        round = int(index / len(USER_AGENTS))
        return USER_AGENTS[(index - (round * len(USER_AGENTS)))]


def get_proxy_ip(driver):
    driver.get('http://ipecho.net/plain')
    ip_address = driver.find_element(By.TAG_NAME, 'pre').text
    return ip_address


# Need to implement
def import_proxies_from_file(file='proxies.txt'):
    logging.info("Loading proxies from {}".format(file))
    try:
        with open(file) as f:
            content = f.readlines()
            content = [x.strip("\n") for x in content]

            proxies = []

            for proxy in content:
                proxy = proxy.split("@")

                if len(proxy) == 2:
                    proxy = (proxy[1], proxy[0])
                else:
                    proxy = (proxy[0], None)

                proxies.append(proxy)

            return proxies

    except Exception as e:
        logging.error(e)


# To debug / test
# Change URL to your country etc..
def add_to_cart(driver, cc='NL'):
    if cc == 'US':
        url = 'http://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-MiniAddProduct?pid=BA8561_560&masterPid=BA8561&Quantity=1&ajax=true'
    else:
        url = 'http://www.adidas.nl/on/demandware.store/Sites-adidas-NL-Site/nl_NL/Cart-MiniAddProduct?pid=BB0945_560&masterPid=BB0945&Quantity=1&ajax=true'

    driver.get(url)
    return url
