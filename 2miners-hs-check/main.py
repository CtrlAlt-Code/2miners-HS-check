import pyodbc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from settings import *
import random
import re
import time

def read_proxies(filename):
    proxies = []
    with open(filename) as file:
        for line in file:
            pr = line.strip()
            m = re.search(r'(.*):(.*):(.*):(.*)', pr)
            if m:
                proxy = f"{m.group(3)}:{m.group(4)}@{m.group(1)}:{m.group(2)}"
                proxies.append(proxy)
    return proxies

def configure_driver(proxy=None):
    print('Configuring driver...')
    options = {
        'proxy': {
            'http': f'http://{proxy}',
            'https': f'https://{proxy}',
            'no_proxy': 'localhost,127.0.0.1'
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

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              seleniumwire_options=options,
                              options=chrome_options)
    return driver

def clean_value(value):
    cleaned_value = re.sub(r'[^\d.]+', '', value)
    return float(cleaned_value) if '.' in cleaned_value else int(cleaned_value)

# Establish connection to SQL Server
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=KEVIN-BATTLE-ST;DATABASE=RVN_DB;Trusted_Connection=yes;')

# Create a cursor
cursor = conn.cursor()

# Example usage:
proxies = read_proxies('proxies.txt')
proxy = random.choice(proxies) if proxies else None
print(f"Using proxy: {proxy}")

# Configure the driver
driver = configure_driver(proxy)

# Load the initial URL
url = "https://rvn.2miners.com/account/RE5Z3zBo5Srx19MY1pBb3kC2UwJNSjZcRX#farms"
print(f"Accessing {url}")
driver.get(url)

try:
    while True:
        time.sleep(2)  # Wait for 2 seconds before collecting data

        unconfirmed_balance = clean_value(driver.find_element(By.XPATH, UNCONFIRMED_BALANCE).text)
        unpaid_balance = clean_value(driver.find_element(By.XPATH, UNPAID_BALANCE).text)
        total_paid = clean_value(driver.find_element(By.XPATH, TOTAL_PAID).text)
        last_24_hours_reward = clean_value(driver.find_element(By.XPATH, LAST_24_HOURS_REWARD).text)
        current_hashrate = clean_value(driver.find_element(By.XPATH, CURRENT_HASHRATE).text)
        average_hashrate = clean_value(driver.find_element(By.XPATH, AVERAGE_HASHRATE).text)
        worker_current_hashrate = clean_value(driver.find_element(By.XPATH, WORKER_CURRENT_HASHRATE).text)
        worker_average_hashrate = clean_value(driver.find_element(By.XPATH, WORKER_AVERAGE_HASHRATE).text)
        worker_reported_hashrate = clean_value(driver.find_element(By.XPATH, WORKER_REPORTED_HASHRATE).text)

        # Insert data into the database
        cursor.execute("INSERT INTO MiningStats (unconfirmed_balance, unpaid_balance, total_paid, last_24_hours_reward, "
                       "current_hashrate, average_hashrate, worker_current_hashrate, worker_average_hashrate, "
                       "worker_reported_hashrate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (unconfirmed_balance, unpaid_balance, total_paid, last_24_hours_reward, current_hashrate,
                        average_hashrate, worker_current_hashrate, worker_average_hashrate, worker_reported_hashrate))

        conn.commit()
        print("Data stored successfully.")

        # Refresh the page every 30 seconds
        time.sleep(28)  # Adjusted to 28 seconds to account for 2 seconds of data collection time
        driver.refresh()

except Exception as e:
    print("An error occurred:", e)
finally:
    # Close the database connection
    conn.close()
