from datetime import datetime as dt
from bs4 import BeautifulSoup
import pg_functions as pg
import discord_post as dp
import requests
import time

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

def check_products(discord_channel, category, subcategory, newegg_category, series = '', page = ''):
    soup = get_soup(f'https://www.newegg.com/p/pl?N={newegg_category}{series}%204131%208000%204814{page}')
    
    if soup.find('span', {'class':'result-message-error'}):
        return False
    else:
        category_dict = {
            'GPU': 1,
            'CPU': 2,
            'Console': 3
        }

        sub_dict = {
            '3060': 4,
            '3060 Ti': 5,
            '3070': 6,
            '3080': 7,
            '3090': 8,
            '6700xt': 9,
            '6800xt': 10,
            '6800': 11,
            '6900xt': 12,
            '5600x': 13,
            '5800x': 14,
            '5900x': 15,
            '5950x': 16
         }

        items = soup.findAll('div', {'class':'item-container'})

        for item in items:
            if item.find('p', {'class':'item-promo'}).text == 'OUT OF STOCK':
                continue

            id = item.find('a', {'class':'item-title'})['href'].split('?')[1][5:]
            link = f'https://newegg.com/p/{id}'
            name = item.find('a', {'class':'item-title'}).text
            price = (item.find('li', {'class':'price-current'}).find('strong').text.replace(',','') + item.find('li', {'class':'price-current'}).find('sup').text)
            image = item.find('img')['src']
            
            dp.discord_webhook_post(discord_channel, subcategory, f'https://secure.newegg.com/Shopping/AddtoCart.aspx?Submit=ADD&ItemList={id}', f'Newegg - ${price}', name, image)
            pg.process_drops([[id, name, 3, category_dict[category], sub_dict[subcategory], price, link, dt.now().strftime('%Y/%m/%d %H:%M:%S'), '', True]])
        
    if soup.find('button', {'class':'btn', 'title':'Next'}):
        pages = soup.find('span', {'class':'list-tool-pagination-text'}).find('strong').text.split('/')

        if pages[0] != pages[1]:
            time.sleep(2)
            page = f'&page={int(pages[0]) + 1}'
            print('\n')
            return check_products(discord_channel, category, subcategory, newegg_category, series, page)
        
def check_ps5_consoles():
    ps5_category = '101696840'
    return check_products('ps5', 'Console', 'ps5', ps5_category)

def check_xbox_consoles():
    xbox_category = '101696839'
    return check_products('xbox', 'Console', 'xbox', xbox_category)

def check_ryzen():
    amd_processors = '50001028'
    ryzen5000series = {
        '5600x':'%20601359147',
        '5800x':'%20601359143',
        '5900x':'%20601362404'
    }
    
    for cpu in ryzen5000series:
        check_products('ryzen', 'GPU', cpu, amd_processors, ryzen5000series[cpu])
        time.sleep(1)

def check_radeon():
    video_cards = '100007709'
    gpus = {
        # '6700xt':'%20601362404',
        '6800':'%20601359427',
        '6800xt':'%20601359422',
        '6900xt':'%20601359957'
    }

    for gpu in gpus:
        check_products('radeon', 'GPU', gpu, video_cards, gpus[gpu])
        time.sleep(1)

def check_rtx():
    video_cards = '100007709'
    gpus = {
        '3060':'%20601361654',
        '3060ti':'%20601359415',
        '3070':'%20601357250',
        '3080':'%20601357247', 
        '3090':'%20601357248'
    }
    
    for gpu in gpus:
        check_products('rtx', 'GPU', gpu, video_cards, gpus[gpu])
        time.sleep(1)

# check_xbox_consoles()
# check_ps5_consoles()
# check_ryzen()
check_rtx()
check_radeon()