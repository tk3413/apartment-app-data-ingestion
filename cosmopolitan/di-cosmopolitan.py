# Python 3 
# (d)ata (i)ngestion.py
# script to scrape cosmopolitan website for apartment data
# author: TK

import json
import requests
import resource
import time
import urllib.request as urllib

from ast import literal_eval
from datetime import datetime
from lxml import html, etree

categories = []
categories.append('2006634')
categories.append('2006635')
categories.append('2006636')
categories.append('2006638')
categories.append('2037059')
categories.append('2006642')
categories.append('2006653')
categories.append('2006654')
categories.append('2007011')
categories.append('2007013')
categories.append('2007021')

url = 'https://www.thecosmopolitanreston.com/availableunits.aspx?myOlePropertyId=456777&MoveInDate=&t=0.5344352604032603&floorPlans='

def loop(url):
#     print(url)
    page = requests.get(url)
# page = requests.get('https://www.thecosmopolitanreston.com/rentaloptions.aspx?UnitID=5075343&FloorPlanID=2006635&myOlePropertyid=456777&MoveInDate=1/31/2020')
    tree = html.fromstring(page.content)
# tree = html.fromstring(page.content)
# text = tree.xpath('/html/body/div[1]/div/div/div[3]/div/div/div/div/section/div/div/div/div[1]/form/div[3]/div[1]/div/div/div[1]/div[2]/div[1]/div/text()')
# print(text)

    item_number = 1
    total_items = 1000

    while(item_number < total_items):
        room_num = tree.xpath('/html/body/div[1]/div/div/div[3]/div/div/div/div/div/div[2]/div[1]/div/div[2]/div/table/tbody/tr[' + str(item_number) + ']/td[1]/text()')
        if room_num == []:
            item_number = total_items
            url = url[:-7]
        else: 
            print(room_num)

        sqft = tree.xpath('/html/body/div[1]/div/div/div[3]/div/div/div/div/div/div[2]/div[1]/div/div[2]/div/table/tbody/tr[' + str(item_number) + ']/td[2]/text()')
        print(sqft)

        price = tree.xpath('/html/body/div[1]/div/div/div[3]/div/div/div/div/div/div[2]/div[1]/div/div[2]/div/table/tbody/tr[' + str(item_number) + ']/td[3]/text()')
        print(price)

        avl_dt = tree.xpath('/html/body/div[1]/div/div/div[3]/div/div/div/div/div/div[2]/div[1]/div/div[2]/div/table/tbody/tr[' + str(item_number) + ']/td[4]/span/text()')
        print(avl_dt)

        item_number+=1
        url = url[:-7]


def send_to_server(apt_nm_cd, apt_num, apt_type, apt_size, apt_price, apt_avl_dt): 
    print('sending to request to server for apt num: ' + apt_num)
    headers = { 'Content-Type': 'application/json' }
    payload = {
            "apt_nm_cd":  apt_nm_cd,
            "apt_num":    apt_num, 
            "apt_type":   apt_type,
            "apt_size":   apt_size,
            "apt_price":  apt_price,
            "apt_avl_dt": apt_avl_dt
    }
    r = requests.post(
        "http://apartment-app-1265692259.us-east-1.elb.amazonaws.com/apartments", 
        # "http://localhost:3000/apartments",
        data = json.dumps(payload),
        headers = headers
    )
    print('post returned status code: ' + str(r.status_code))
    if(str(r.status_code) == '201'):
        print('new apartment or price changed for ' + apt_nm_cd + ' apt number: ' + apt_num)
        return 1
    else: 
        return 0

for category in categories:
    loop(url=url+category) 
    