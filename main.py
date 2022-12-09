from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup

# page's HTML code
html_text = requests.get('https://coinmarketcap.com/').text

soup = BeautifulSoup(html_text, 'lxml')
crypto_table = soup.find('div', class_="sc-f7a61dda-2 efhsPu")
crypto_names = crypto_table.find_all('p', class_="sc-e225a64a-0 ePTNty")

latest_prices = [0.0 for i in range(len(crypto_names))]
price_diff = ["" for i in range(len(crypto_names))]
run_count = 0


# loop for auto retrieval
while 1:
    run_count += 1
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"Time: {current_time}, run count: {run_count}\n")

    html_text = requests.get('https://coinmarketcap.com/').text

    soup = BeautifulSoup(html_text, 'lxml')

    crypto_table = soup.find('div', class_="sc-f7a61dda-2 efhsPu")
    crypto_names = crypto_table.find_all('p', class_="sc-e225a64a-0 ePTNty")
    crypto_symbols = crypto_table.find_all('p', class_="sc-e225a64a-0 dfeAJi coin-item-symbol")
    crypto_prices = crypto_table.find_all('div', class_="sc-7510a17-0 hEduBL")

    current_prices = [float(i.text[1:].replace(',', '')) for i in crypto_prices]

    if run_count > 1:
        price_diff = []
        for i in range(len(crypto_names)):
            current_price = current_prices[i]
            # print(current_price, latest_prices[i])
            if current_price == latest_prices:
                price_diff.append('')
            else:
                k = current_price - latest_prices[i]
                if k > 0:
                    price_diff.append(f"🔺${abs(k)}")
                elif k < 0:
                    price_diff.append(f"🔻${abs(k)}")
                else:
                    price_diff.append("No change")

    for i in range(len(crypto_names)):
        print(f"{crypto_names[i].text}, {crypto_symbols[i].text}: {crypto_prices[i].text}, ", end=" ")
        print(price_diff[i])
    print('------------- \n')

    latest_prices = current_prices

    # retrieves data in every 5 minutes
    time.sleep(5*60)

