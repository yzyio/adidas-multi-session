import logging, threading, time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from config import PROXIES, USE_PROXIES, NUM_SESSIONS, CHROMEDRIVER_LOCATION, PHANTOM_JS_LOCATION
from utils import check_if_valid_url, get_proxy, get_user_agent, check_if_past_queue, add_to_cart
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC


# For every session we want to load the product page / queue for cookies
def load_session(driver, url):
    try:
        driver.get(url)
        logging.info("Product page loaded on session: {}".format(driver.session_id))
    except TimeoutException:
        logging.error("Page load time out on session: {}".format(driver.session_id))


def transfer_session(driver, proxy, proxy_auth, user_agent):
    logging.info("[New Thread] Transferring session {}".format(driver.session_id))

    url = driver.current_url
    chrome_options = Options()
    chrome_options.add_argument("user-agent={}".format(user_agent))

    if USE_PROXIES:
        chrome_options.add_argument("--proxy-server=http://{}".format(proxy))

    chrome = webdriver.Chrome(executable_path=CHROMEDRIVER_LOCATION, chrome_options=chrome_options)

    # Open URL and wait for proxy login
    chrome.get(url)

    if USE_PROXIES:
        logging.info("[CHROME/PROXY] Login with {}".format(proxy_auth))

        chrome.implicitly_wait(10)
        element = WebDriverWait(chrome, 1000).until(EC.presence_of_element_located((By.TAG_NAME, "div")))

    # Transfer Cookies
    chrome.delete_all_cookies()
    for cookie in driver.get_cookies():
        chrome.add_cookie(cookie)

    chrome.refresh()


def run(url):
    valid_url = check_if_valid_url(url)
    if not valid_url:
        print("=> Invalid URL, must start with http://www.\n")
    else:
        print("=> URL is valid\n")

    drivers = []
    for session_num in range(0, len(PROXIES) if USE_PROXIES else NUM_SESSIONS):
        service_args = []
        if USE_PROXIES:
            proxy, proxy_auth = get_proxy(session_num)
            service_args = [
                '--proxy={}'.format(proxy),
                '--proxy-type=http',
                '--ignore-ssl-errors=true',
            ]

            if proxy_auth:
                service_args.append('--proxy-auth={}'.format(proxy_auth))

            logging.debug(service_args)

        user_agent = get_user_agent(session_num)
        desired_capabilities = dict(DesiredCapabilities.PHANTOMJS)
        desired_capabilities['phantomjs.page.settings.userAgent'] = user_agent
        desired_capabilities['phantomjs.page.customHeaders.User-Agent'] = user_agent
        desired_capabilities['phantomjs.page.customHeaders.customHeaders'] = \
            {'Accept': 'text/html', 'Content-type': 'text/html', 'Cache-Control': 'max-age=0'}

        driver = webdriver.PhantomJS(executable_path=PHANTOM_JS_LOCATION, service_args=service_args)
        driver.set_page_load_timeout(30)

        drivers.append(driver)

    for driver in drivers:
        load_session(driver, url)

    # Now the product pages are loaded, we are just gonna check if the hmac cookie is set on one of our session
    # If true we want to transfer the session to a Chrome browser to let you check-out
    opened_drivers = []
    while True:
        logging.info("Checking for hmac in all session cookies.. [10s interval]")
        for session_num, driver in enumerate(drivers):
            if check_if_past_queue(driver) and driver not in opened_drivers:
                opened_drivers.append(driver)

                logging.info("[HMAC] Cookie found on session {}".format(driver.session_id))

                # New thread open browser
                user_agent = get_user_agent(session_num)
                if USE_PROXIES:
                    proxy, proxy_auth = get_proxy(session_num)
                else:
                    proxy = None
                    proxy_auth = None

                threading.Thread(target=transfer_session, kwargs={
                    'driver': driver,
                    'proxy': proxy,
                    'proxy_auth': proxy_auth,
                    'user_agent': user_agent
                }).start()

        time.sleep(10)
