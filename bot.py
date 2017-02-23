import logging, threading, time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

from utils import write_cookies_to_file, find_path

opened_sessions = []


def transfer_session(browser):
    driver = browser['browser']
    logging.info("[New Thread] Transferring session {}".format(driver.session_id))

    # Save cookies
    write_cookies_to_file(driver.get_cookies())

    url = driver.current_url

    chrome_options = Options()
    chrome_options.add_argument("user-agent={}".format(browser['user_agent']))
    chrome_options.add_argument("--proxy-server=http://{}".format(browser['proxy'][0]))
    chrome = webdriver.Chrome(executable_path=find_path('chromedriver'), chrome_options=chrome_options)

    # Open URL and wait for proxy login
    chrome.get(url)
    logging.info("[CHROME/PROXY] Login with {}".format(browser['proxy'][1]))

    chrome.implicitly_wait(10)
    element = WebDriverWait(chrome, 1000).until(EC.presence_of_element_located((By.TAG_NAME, "div")))

    # Transfer Cookies
    chrome.delete_all_cookies()
    for cookie in driver.get_cookies():
        chrome.add_cookie(cookie)

    chrome.refresh()
    time.sleep(10000)


def start_session(url, browser):
    global opened_sessions

    # empty the cookies file
    open('cookies.txt', 'w').close()

    while True:
        if browser['browser'].session_id not in opened_sessions:
            logging.info("Checking if session {} is past splash".format(browser['browser'].session_id))

            tries = 0
            while tries < 5:
                # Check for captcha field
                try:
                    captcha = "captcha-container clearfix" in browser['browser'].page_source.lower()

                    if captcha:
                        opened_sessions.append(browser['browser'])
                        threading.Thread(target=transfer_session, kwargs={'browser': browser}).start()
                        return False
                except:
                    pass

                # Check cookies
                hmac_cookie_exists = False
                for cookie in browser['browser'].get_cookies():
                    hmac_cookie_exists = True if 'hmac=' in cookie['value'] or 'gceeqs' == cookie['name'] else False

                    if hmac_cookie_exists:
                        break

                if hmac_cookie_exists:
                    opened_sessions.append(browser['browser'])
                    threading.Thread(target=transfer_session, kwargs={'browser': browser}).start()
                    return False
                else:
                    # Delete cookies and try again, seems to work these days
                    browser['browser'].delete_all_cookies()
                    browser['browser'].refresh()
                    tries += 1

                time.sleep(10)


def run(url, faceless_browsers):
    for browser in faceless_browsers:
        threading.Thread(target=start_session, kwargs={'url': url, 'browser': browser}).start()
