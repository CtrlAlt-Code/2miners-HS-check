from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import random
import re
import time


def read_proxies(filename):
    scheme = 'http'
    proxies = []
    with open(filename) as file:
        for line in file:
            pr = line.strip()
            m = re.search(r'(.*):(.*):(.*):(.*)', pr)
            if m:
                # Format for seleniumwire: 'username:password@host:port'
                proxy = f"{m.group(3)}:{m.group(4)}@{m.group(1)}:{m.group(2)}"
                proxies.append(proxy)
    return proxies


def configure_driver(proxy=None):
    print('Configuring driver...')
    options = {
        'proxy': {
            'http': f'http://{proxy}',
            'https': f'https://{proxy}',
            'no_proxy': 'localhost,127.0.0.1'  # Exclude localhost and 127.0.0.1 from proxying
        }
    }
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = False
    chrome_options.add_argument('start-maximized')
    chrome_options.add_argument("window-size=1900,1080")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/87.0.4280.141 Safari/537.36"
    )

    # Use seleniumwire's webdriver with seleniumwire_options
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              seleniumwire_options=options,
                              options=chrome_options)
    return driver


# Example usage:
proxies = read_proxies('proxies.txt')
proxy = random.choice(proxies) if proxies else None
print(f"Using proxy: {proxy}")

# Configure driver with proxy
driver = configure_driver(proxy)

# Use driver.get(URL) to navigate to the page
url = "https://rvn.2miners.com/account/RE5Z3zBo5Srx19MY1pBb3kC2UwJNSjZcRX#farms"
print(f"Accessing {url}")
driver.get(url)

# Add a delay to observe the browser or wait for necessary elements
time.sleep(10)

driver.quit()
