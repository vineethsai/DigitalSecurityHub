from bs4 import BeautifulSoup
import requests
import json
import random

data = {

    }
data['product'] = []

def retrieve_all_products(category):
    if category == "Protect and Prevent":
        page = requests.get("https://www.business.att.com/categories/protect-and-prevent.html")
    elif category == "Detect and Respond":
        page = requests.get("https://www.business.att.com/categories/detect-and-respond.html")
    elif category == "Assess and Plan":
        page = requests.get("https://www.business.att.com/categories/assess-and-plan.html")

    soup = BeautifulSoup(page.content, 'html.parser')    
    titles = soup.find_all(class_="matchscore-product-title")
    descs = soup.find_all(class_="matchscore-product-desc")
    prices = soup.find_all(class_="matchscore-product-price")
    for title, desc, price in zip(titles, descs, prices):
        price_val = 0
        if not price.get_text() == ' ':
            price_val = float(price.get_text().strip().replace(",", '')[1:])
        data['product'].append({
            'title' : title.get_text(),
            'description': desc.get_text(),
            'category': category,
            'price': price_val,
            'active': True,
            'stock': random.randint(1,99),
            'seller_id': 5
        }) 

if __name__ == '__main__':
    retrieve_all_products("Protect and Prevent")
    retrieve_all_products("Detect and Respond")
    retrieve_all_products("Assess and Plan")
    json_file = json.dumps(data)
    print(json_file)