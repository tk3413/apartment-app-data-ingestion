# Python 3 
# (d)ata (i)ngestion.py
# script to scrape vita website for apartment data
# author: TK

import json
import requests
import resource
import time

from ast import literal_eval
from datetime import datetime
from lxml import html

# formatters 
def replace_all(text, replacements):
    """
    PARAMETERS:
        text: 
            type: string 
            description: any string to be scrubbed 
            example: '$1,000 /Month'  
        dic: 
            type: dictionary
            description: in a dictionary, capture replacements in the format
            {"string_to_be_replaced":"replacement_string"}
            example: {"$":"", "/Month":""}
    RETURNS:
        text: 
            type: string
            description: original text (parameter) with substitutions 
            as outlined in replacements (parameter)
            example: '1000'
    """
    for i, j in replacements.items():
        text = text.replace(i, j)
    return text

def apt_num_format(tree, item_num):
    apt_num = tree.xpath('//div[' + str(item_num) + ']/a/figure/figcaption/div/h2/text()')
    return str(apt_num[0])

def apt_price_format(tree, item_num): 
    path_price = tree.xpath('//div[' + str(item_num) + ']/a/figure/figcaption/div/ul/li[4]/text()')
    apt_price = path_price[0].split()
    replacements = { "/Month": "", "$": "" }
    apt_price_cleaned = replace_all(apt_price[1], replacements)
    return str(apt_price_cleaned)

def apt_type_format(tree, item_num):
    path_apt_type = tree.xpath('//div[' + str(item_num) + ']/a/figure/figcaption/div/ul/li[1]/text()')
    return str(path_apt_type[0])

def apt_size_format(tree, item_num):
    path_apt_size = tree.xpath('//div[' + str(item_num) + ']/a/figure/figcaption/div/ul/li[3]/text()')
    return str(path_apt_size[0])

def apt_avail_dt_format(tree, item_num): 
    path_apt_avail_dt = tree.xpath('//div[' + str(item_num) + ']/a/figure/figcaption/div/ul/li[5]/text()')
    apt_avail_dt = path_apt_avail_dt[0]
    replacements = { "Available": ""}
    apt_avail_dt_cleaned = replace_all(apt_avail_dt, replacements)
    if apt_avail_dt_cleaned == ' Now':
        apt_avail_dt_cleaned = time.strftime('%b %d, %Y')
    return str(apt_avail_dt_cleaned.strip())

def vita_page_format(tree): 
    path_num_pages = tree.xpath('/html/body/div/div[2]/div/section[2]/div[4]/div/div[8]/span/span/text()')
    total_num_pages = path_num_pages[0].strip()[10]
    return int(total_num_pages)

def formatter(format_type, tree, item_num):
    return {
        'TOTAL_PG':     vita_page_format(tree),
        'APT_NUM':      apt_num_format(tree, item_num),
        'APT_TYPE':     apt_type_format(tree, item_num),
        'APT_SIZE':     apt_size_format(tree, item_num),
        'APT_PRICE':    apt_price_format(tree, item_num),
        'APT_AVAIL_DT': apt_avail_dt_format(tree, item_num)
    }.get(format_type, "Invalid format_type")

# helper functions
def get_constant(key):
    constants = { 
        "apt_nm_cd": "VITA",
        "base_url": 'https://www.vitatysons.com/floor-plans/',
        "default_query_params": "?floor=&max=&bedrooms=0&bedrooms=1&bedrooms=2&bedrooms=3&min=&availability="
    }

    if key in constants:
        return constants[key]
    else:
        raise ValueError(key + ' was not found in list of constants')

def get_total_pages(): 
    page = requests.get(get_constant('base_url') + get_constant('default_query_params') + '&page=' + str(2))
    tree = html.fromstring(page.content)
    total_num_pages = vita_page_format(tree)
    print('total number of pages is: ' + str(total_num_pages))
    return total_num_pages

def send_to_server(apt_nm_cd, apt_num, apt_type, apt_size, apt_price, apt_avl_dt, cret_ts): 
    print('sending to request to server for apt num: ' + apt_num)
    headers = { 'Content-Type': 'application/json' }
    payload = {
            "apt_nm_cd":  apt_nm_cd,
            "apt_num":    apt_num, 
            "apt_type":   apt_type,
            "apt_size":   apt_size,
            "apt_price":  apt_price,
            "apt_avl_dt": apt_avl_dt,
            "cret_ts":    cret_ts
    }
    r = requests.post(
        "http://apartment-app-1265692259.us-east-1.elb.amazonaws.com/apartments", 
        data = json.dumps(payload),
        headers = headers
    )
    print('post returned status code: ' + str(r.status_code))
    if(str(r.status_code) == '201'):
        print('new apartment or price changed for ' + apt_nm_cd + ' apt number: ' + apt_num)
        return 1
    else: 
        return 0

# main logic
current_page_num = 1
total_num_pages = get_total_pages()
base_url = get_constant('base_url')
default_query_params = get_constant('default_query_params')

now = datetime.now()
formatted_now = now.strftime("%m/%d/%Y %H:%M:%S")
print ('execution timestamp: ' + formatted_now)

total_new_apartments = 0
while(current_page_num <= total_num_pages):
    # for each page, create a new tree to parse below
    print('\nPage: ' + str(current_page_num))
    page_param = '&page=' + str(current_page_num) + ''
    full_path = base_url + default_query_params + page_param
    page = requests.get(full_path)
    tree = html.fromstring(page.content)
    print('hello')
    # 6 items per page, range of required values = [2, 7]
    item_num = 2
    
    # send each item to db via server
    while(item_num < 8): 
        total_new_apartments += send_to_server(
            get_constant('apt_nm_cd'),
            formatter('APT_NUM',      tree, item_num), 
            formatter('APT_TYPE',     tree, item_num),
            formatter('APT_SIZE',     tree, item_num),
            formatter('APT_PRICE',    tree, item_num),
            formatter('APT_AVAIL_DT', tree, item_num),
            formatted_now
        )
        item_num += 1
    current_page_num += 1

print('\ntotal new apartments added from this execution: ' + str(total_new_apartments))