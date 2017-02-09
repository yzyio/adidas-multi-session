import sys, logging

if sys.version_info <= (3, 0):
    sys.stdout.write("Could not start: requires Python 3.x, not Python 2.x\n")
    sys.exit(1)

if __name__ == '__main__':
    from bot import run
    from config import PRODUCT_URL, PROXIES, _V, USE_PROXIES

    url = PRODUCT_URL
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

    # General output information before start, (tbh need to art ASCII art)
    print("\nAdidas Multi Session by YZY.io (BETA) \n"
          "Thank you for testing the script, you are on version {}\n".format(_V))
    print("Proxies loaded: {}".format(len(PROXIES)))

    if USE_PROXIES and len(PROXIES) == 0:
        print("USE_PROXIES = True but no proxies loaded..")
        sys.exit(1)

    if PRODUCT_URL is not '' or not None:
        url = PRODUCT_URL
        print("Product URL: {}".format(PRODUCT_URL))
    else:
        url = input("Product URL: ")

    run(url)
