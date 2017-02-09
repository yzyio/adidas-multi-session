import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from config import PHANTOM_JS_LOCATION, CHROMEDRIVER_LOCATION
from utils import get_proxy, get_user_agent, add_to_cart
from bot import transfer_session
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def _transfer_test():
    PROXY_INDEX = 0

    # Session Transfer Testing
    proxy, proxy_auth = get_proxy(PROXY_INDEX)
    service_args = ['--proxy={}'.format(proxy), '--proxy-type=html', '--ignore-ssl-errors=true']
    if proxy_auth:
        service_args.append('--proxy-auth={}'.format(proxy_auth))

    driver = webdriver.PhantomJS(executable_path=PHANTOM_JS_LOCATION, service_args=service_args)
    add_to_cart(driver, cc='US')

    # Test transferring session (go to ipecho.net to see ip, got to cart to see if in cart)
    transfer_session(driver, proxy, proxy_auth, user_agent=get_user_agent(PROXY_INDEX))

    time.sleep(60 * 60)


def _test_phantomjs_dynamic_cookies():
    # Use http://tools.yzy.io/hmac.html as PRODUCT_URL to test
    # That page wil set a (fake) hmac cookie after 10 seconds
    pass

_transfer_test()
