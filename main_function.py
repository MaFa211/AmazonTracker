from Amazon_Tracker import AmazonTracker, DataBase

# Create instances
tracker = AmazonTracker("url.csv")
database = DataBase(db_name="tracking.db", table_name="results")

# Create Database
database.create_database()

# Scrape and save results
for element in tracker.url_list:
    request = tracker.get_request(element)
    title = tracker.get_product_title(request)
    price = tracker.get_price(request)
    date = tracker.get_date()
    if tracker.is_availabe(request):
        database.add_record(product_title=title, price=price, date=date)
    else:
        database.add_record(product_title=title, price="Not Availabe", date=date)
    #database.show_results()

    #['https', 'http://80.48.119.28:8080']