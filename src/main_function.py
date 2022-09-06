from Amazon_Tracker import AmazonTracker, DataBase, RequestData
import time
import logging

# Need to log bad requests
logging.basicConfig(filename='logging.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


# Create instances
tracker = AmazonTracker("url.csv")
database = DataBase(db_name="tracking.db", table_name="results")
request_data = RequestData()

# Create Database
database.create_database()


#@repeat(every(10).minutes)

# Scrape and save results
while True:
    for element in tracker.url_list:
        try:
            user_agent = request_data.get_single_useragent()
            proxy = request_data.get_single_proxy()
            request = tracker.get_request('https://httpstat.us/404', user_agent, proxy)
        except Exception as Argument:
            logging.exception("Error occurred while requesting urls")
        title = tracker.get_product_title(request)
        price = tracker.get_price(request)
        date = tracker.get_date()
        if tracker.is_availabe(request):
            database.add_record(product_title=title, price=price, date=date)
        else:
            database.add_record(product_title=title, price="Not Availabe", date=date)
        time.sleep(60*60)




