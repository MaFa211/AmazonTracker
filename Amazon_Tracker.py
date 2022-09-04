# Dependencies
import time
from requests_html import HTMLSession
from requests_html import user_agent
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3
import random
import os.path

import re


class AmazonTracker:
    def __init__(self, url_list_name):
        self.url_list = self.get_url_list(url_list_name)

    # Import Url List
    def get_url_list(self, url_list_name):
        url_list = []
        with open(url_list_name, "r") as f:
            for row in f:
                url_list.append(row)
        return(url_list)

# Get Request
    def get_request(self, url):
        s = HTMLSession()
        proxy = get_random_proxy()
        fake_agent = user_agent()
        fake_agent = {'user_agent': get_user_agent()}
        request = s.get(url, proxies={proxy[0]: proxy[1]}, headers=fake_agent)
        time.sleep(random.randint(1, 10))
        if request.status_code!=200:
            return("Request Failed!")
        parsed_request = BeautifulSoup(request.content, 'html.parser')
        with open("request.html", "w") as f:
            f.write(str(parsed_request))
        return(parsed_request)



    # Check if product is availabe
    def is_availabe(self, parsed_request):
        if "Request Failed!" in parsed_request:
            return False
        available_div = parsed_request.find(id = "buybox")
        available_check = available_div.get_text(strip = True)
        if "Derzeit nicht verfügbar" in available_check:
            return False
        else:
            return True


    # Find price in parsed request
    def get_price(self, parsed_request):
        price_div = parsed_request.find(id = "buybox")
        if price_div is None:
            price_div = parsed_request.find(id = "priceblock_saleprice")
        price_string = str(price_div.get_text(strip=True))
        print(type(price_string))
        pattern = re.compile("\d+(\,\d{2})?")
        try:
            r = re.search(pattern, price_string)
            price = r.group()
        except AttributeError:
            price = "Not Available"
        return price


    # Getting product title and description (which is one string) from parsed request
    def get_product_title(self, parsed_request):    
        title_div = parsed_request.find(id = "title")
        title_string = title_div.get_text(strip=True)
        title_string = title_string.replace("\xa0", "")
        return(title_string)

    # Getting the time when the request is made
    def get_date(self):
        now = datetime.now()
        date = now.strftime("%d/%m/%Y %H:%M:%S")
        return(date)

    # Combining availability and price functions to get an actual price
    # def get_price(self, parsed_request):
    #     if self.is_availabe(parsed_request):
    #         price_div = find_price(parsed_request)
    #         price = format_price(price_div)
    #     else:
    #         price = "Not Available"
    #     return(price)


class DataBase:
    def __init__(self, db_name: str, table_name: str):
        self.db_name = db_name
        self.table_name = table_name

    def create_database(self):
        if not os.path.exists(self.db_name):
            connection = sqlite3.connect(self.db_name)
            c = connection.cursor()
            c.execute(f"""
                    CREATE TABLE {self.table_name}(
                        product_title text,  
                        price real,
                        date text)                        
                        """)
            connection.commit()
            connection.close()
        else:
            print("Database already exists")

    def add_record(self, product_title, price, date):
        connection = sqlite3.connect(self.db_name)
        c = connection.cursor()
        c.execute(f"INSERT INTO {self.table_name} VALUES (?,?,?)", (product_title, price, date))
        connection.commit()
        connection.close()

    def show_results(self):
        connection = sqlite3.connect(self.db_name)
        c = connection.cursor()
        c.execute(f"SELECT rowid, * FROM {self.table_name}")
        items = c.fetchall()
        for content in items:
            print(content)
        connection.commit()
        connection.close()


class RequestData:
    proxy_url = "https://free-proxy-list.net/"

    def __init__(self):
        self.proxy_list = RequestData.get_proxy_list()
        self.proxy_counter = 0
        self.user_agent_list = RequestData.get_user_agent_list()
        self.agent_counter = 0

    @staticmethod
    def get_proxy_list():
        s = HTMLSession()
        request = s.get(RequestData.proxy_url)
        parsed_request = BeautifulSoup(request.content, "html.parser")
        proxy_table = parsed_request.find("tbody")
        proxy_table_rows = proxy_table.find_all("tr")
        tds = list()
        for tr in proxy_table_rows:
            tds.append(tr.find_all("td"))

        for i in range(0, len(tds)):
            for j in range(0, 2):
                tds[i][j] = tds[i][j].get_text()

        proxies = []
        for i in range(0, len(tds)):
            ip = tds[i][0]
            port = tds[i][1]
            if "yes" in tds[i][5].get_text():
                #http:// irrespective of encrypted connection or not
                proxies.append(['https', f'http://{ip}:{port}'])
            else:
                proxies.append(['http', f'http://{ip}:{port}'])
        return proxies

    @staticmethod
    def get_user_agent_list():
        url = "https://user-agents.net/random"
        s = HTMLSession()
        request = s.get(url)
        parsed_request = BeautifulSoup(request.content, "html.parser")
        user_agents = str(parsed_request.find('ol').get_text())
        user_agent_list = user_agents.splitlines()
        return user_agent_list

    
    def get_single_proxy(self):
        if self.proxy_counter < len(self.proxy_list):
            self.proxy_counter += 1
            return self.proxy_list[self.proxy_counter]
        else:
            self.proxy_list = RequestData.get_proxy_list()
            self.proxy_counter = 0
            return self.proxy_list[self.proxy_counter]


    def get_single_useragent(self):
        if self.agent_counter < len(self.proxy_list):
            self.agent_counter += 1
            return self.user_agent_list[self.agent_counter]
        else:
            self.user_agent_list = RequestData.get_proxy_list()
            self.proxy_counter = 0
            return self.proxy_list[self.proxy_counter]








