import sys, logging
from utils import find_path

_V = '0.22'
PRODUCT_URL = 'http://www.adidas.com/yeezy'
# PRODUCT_URL = 'http://tools.yzy.io/hmac.html'

if sys.version_info <= (3, 0):
    sys.stdout.write("Could not start: requires Python 3.x, not Python 2.x\n")
    sys.exit(1)

if __name__ == '__main__':
    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.wait import WebDriverWait

    from bot import run
    from utils import import_proxies_from_file, get_user_agent, get_desired_capabilities_phantom

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

    # General output information before start, (tbh need to art ASCII art)
    print("\nAdidas Multi Session by YZY.io (BETA) (V{})".format(_V))

    # Load proxies
    proxies = import_proxies_from_file()

    if proxies is None:
        print("Could not load proxies, make sure you use the proxies.txt file and use the right format.")
        sys.exit(1)

    print("Proxies loaded: {}".format(len(proxies)))

    # Test proxies and create drivers
    faceless_browsers = []
    for i, proxy in enumerate(proxies):
        proxy_auth = proxy[1]
        service_args = [
            '--proxy={}'.format(proxy[0]),
            '--proxy-type=http',
            '--ignore-ssl-errors=true'
        ]

        if proxy_auth:
            service_args.append('--proxy-auth={}'.format(proxy_auth))

        print("")
        logging.info("[{}/{}] Testing proxy: {}".format(i + 1, len(proxies), proxy))

        user_agent = get_user_agent()
        desired_capabilities = get_desired_capabilities_phantom(user_agent)
        browser = webdriver.PhantomJS(executable_path=find_path('phantomjs'), service_args=service_args, desired_capabilities=desired_capabilities)
        browser.set_page_load_timeout(30)

        # Proxy testing
        try:
            browser.get('http://tools.yzy.io/ip.php')
            element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            if not element:
                logging.error('[{}/{}] Proxy could not load URL: {}'.format(i + 1, len(proxies), 'http://ipecho.net/plain'))
                continue

            logging.info('[{}/{}] Proxy using IP: {}'.format(i + 1, len(proxies), element.text))
        except TimeoutException:
            logging.error('[{}/{}] Proxy Time-out: {}'.format(i + 1, len(proxies), proxy))
            continue
        except Exception as e:
            logging.error('[{}/{}] {}'.format(i + 1, len(proxies), e))
            continue

        try:
            browser.get(PRODUCT_URL)

            if ('you have been blocked' in browser.page_source.lower()) or ('a security issue was automatically identified' in browser.page_source.lower()):
                logging.error('[{}/{}] Proxy Banned on {}'.format(i + 1, len(proxies), PRODUCT_URL))
                continue

            element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, "div")))
            if not element:
                logging.error('[{}/{}] Proxy could not load URL: {}'.format(i + 1, len(proxies), PRODUCT_URL))

            logging.info('[{}/{}] Proxy Test Success'.format(i + 1, len(proxies)))

            faceless_browsers.append({
                'browser': browser,
                'user_agent': user_agent,
                'proxy': proxy
            })
        except TimeoutException:
            logging.error('[{}/{}] Proxy Time-out: {}'.format(i + 1, len(proxies), proxy))
            continue
        except Exception as e:
            logging.error('[{}/{}] {}'.format(i + 1, len(proxies), e))
            continue

    if len(faceless_browsers) > 0:
        print("\nWorking proxies: {} - starting script..".format(len(faceless_browsers)))

        run(PRODUCT_URL, faceless_browsers)
    else:
        print("\nNo working proxies found.")
