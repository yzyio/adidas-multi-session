<b>Current version:</b> V0.22 (beta)

<p align="center"><img src="http://tools.yzy.io/assets/github.png"></p>

adidas-multi-session is a open-source program to simulate multiple sessions on adidas queue pages.
It will open a x amounts of sessions in the background (depending on the num of proxies), when a session gets past queue/splash,
it will automatically open a Chrome window with the active session. This script is still in BETA and doesn't guarantee any 'cart'. It is actively developed.

For updates follow me on Twitter: <a href="http://twitter.com/TerryBommels">@TerryBommels</a> and follow YZY.io on Twitter: <a href="http://twitter.com/yzyio">@yzyio</a>

#### License
This script is licensed under <a href="https://tldrlegal.com/license/non-profit-open-software-license-3.0-(nposl-3.0)">NPOSL-3.0</a>. A short summary of this license is:

* It can only be used as non-profit
* Your code must be open-source, even modifications of the code

#### Requirements
You need the following things installed on your Windows/Mac/Linux computer:

* Python 3+, download <a href="https://www.python.org/downloads/">here</a>
* A PhantomJS file (.exe/.dmg), download <a href="http://phantomjs.org/download.html">here</a>
* A chromedriver file (.exe/.dmg), download <a href="https://chromedriver.storage.googleapis.com/index.html?path=2.9/">here</a>

## Installation
### First time instructions
If you use this script for the first time, following these instructions. Make sure you are always on the latest version:

* Download or clone this repository. And put it in a folder.
* Open a cmd/terminal window and go to the folder where the project files are located.
* Run `pip install -r requirements.txt`
* Put the PhantomJS(.exe for windows) and chromedriver(.exe for windows) in the adidas-multi-session folder.
* Run `python run.py` in cmd/terminal to start the script.

### Update instructions

* Download/clone this repository. Overwrite existing files.
* Run `pip install -r requirements.txt`
* Run `python run.py` in cmd/terminal to start the script.


### About

* Every x seconds the script will check for the hmac cookie or captcha field.
* If not found it will delete all cookies and try again, maximum 5 times and than try next IP/Proxy.
* If the cookie is found, the session will be transferred to a Chrome session.
* If you are using a proxy with authentication, you need to login first. The credentials are printed in the console.
* It will load the page with the cookies / ip / user-agent from the session that got past splash.
* If any problem occurs the cookies are also saved to cookies.txt. If there is no option to select size after opening chrome try adding it through wishlist or with Solemartyr's script.


## Extra
For questions, please do not DM me. You can write a public tweet to me and I will reply. I will accept pull requests so feel free to contribute.

### Frequently asked questions
#### Does this work?
It is never tested on a live release. So it is possible it won't work at all, will crash or let you cop a pair. It only increases your chances and is no 'bypass'.
A 'bypass' does not exists (atm) and all the popular ATC/Cook Groups/Mafias are using this same method but on a much larger scale.

#### Do I really need proxies?
Yes. Using the same IP doesn't make a difference.

#### Where can I buy proxies?
MyPrivateProxy (MPP): <a href="https://www.myprivateproxy.net/billing/aff.php?aff=1840">Website</a>.

I will update this README with more proxy providers. Make sure you pick sneaker proxies that work on adidas (for MPP).

#### I get Python 2/3 errors / Selenium says it's not installed
Make sure you use Python <b>3</b>. Run pip -V to see your Python version. If it says Python 2 search on Google how to change your default Python version for your platform.

### Disclaimer
Use at your own risk.
