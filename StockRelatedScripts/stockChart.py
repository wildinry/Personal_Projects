import requests
from bs4 import BeautifulSoup
import csv
import time
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def scrape_yahoo_finance(url):
    headers = {'User-Agent': 
'RBExampleStocktoGraphScrape'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        print("Failed to retrieve page:", response.status_code)
        return None

def extract_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    name_element = soup.find('h1', class_='D(ib)')
    price_element = soup.find('fin_streamer', class_='livePrice svelte-mgkamr')
    name = name_element.text.strip() if name_element else None
    price = price_element.text.strip().replace(',', '') if price_element else None
    return name, price
def write_to_csv(name, price, date):
    file_path = 'yahoo_finance_data2.csv'
    data = {'Name': name, 'Price': price, 'Date': date}
    mode = 'a' if os.path.exists(file_path) else 'w'
    with open(file_path, mode=mode, newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if mode == 'w':
            writer.writeheader()
        writer.writerow(data)

def plot_prices(prices_dict):
    for name, prices in prices_dict.items():
        dates = range(1, len(prices) + 1)
        plt.scatter(dates, prices, label=name)
    plt.title('Stock Prices Over Time')
    plt.xlabel('Days')
    plt.ylabel('Price')
    plt.legend()
    plt.show()


while True:
    run_for = 1  # run for 1 day
    url_list = ["https://finance.yahoo.com/quote/SOUN/", "https://finance.yahoo.com/quote/NVDA/", "https://finance.yahoo.com/quote/AAPL/"]
    prices_dict = {name: [] for name in url_list}  # Dictionary to store prices for each stock

    end_date = datetime.now() + timedelta(days=run_for)
    current_date = datetime.now()

    while current_date <= end_date:
        for url in url_list:
            html_content = scrape_yahoo_finance(url)
            if html_content:
                name, price = extract_data(html_content)
                print(name, price)
                if price is not None:
                    write_to_csv(name, price, current_date.strftime('%Y-%m-%d'))
                    prices_dict[url].append(float(price))
                    print("Data written to CSV file")
                else:
                    print("Price not available for", name)
            else:
                print("Failed to retrieve HTML content.")
        current_date += timedelta(days=1)  # Move to the next day
    time.sleep(60*5)
    plot_prices(prices_dict)

