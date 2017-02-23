import time, threading

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from utils import import_proxies_from_file, get_user_agent
from bot import transfer_session
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def add_to_cart(driver, cc='NL'):
    if cc == 'US':
        url = 'http://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-MiniAddProduct?pid=BA8561_560&masterPid=BA8561&Quantity=1&ajax=true'
    else:
        url = 'http://www.adidas.nl/on/demandware.store/Sites-adidas-NL-Site/nl_NL/Cart-MiniAddProduct?pid=BB0945_560&masterPid=BB0945&Quantity=1&ajax=true'

    driver.get(url)

    return url


def _transfer_test():
    # which proxy to use? 0 = first
    # TODO: add a better way to specify the proxy
    PROXY_INDEX = 0

    # Session Transfer Testing
    PROXIES = import_proxies_from_file()

    proxy, proxy_auth = PROXIES[PROXY_INDEX]
    service_args = ['--proxy={}'.format(proxy), '--proxy-type=html', '--ignore-ssl-errors=true']
    if proxy_auth:
        service_args.append('--proxy-auth={}'.format(proxy_auth))

    browser = webdriver.PhantomJS(executable_path='bin/phantomjs', service_args=service_args)
    browser.set_page_load_timeout(30)

    add_to_cart(browser, cc='US')

    payload = {
        'browser': browser,
        'user_agent': get_user_agent(),
        'proxy': proxy
    }

    # Test transferring session (go to ipecho.net to see ip, got to cart to see if in cart)
    threading.Thread(target=transfer_session, kwargs={'browser': payload}).start()

    time.sleep(60 * 60)


def _test_phantomjs_dynamic_cookies():
    # Use http://tools.yzy.io/hmac.html as PRODUCT_URL to test
    # That page will set a (fake) hmac cookie after 10 seconds
    pass


_transfer_test()
