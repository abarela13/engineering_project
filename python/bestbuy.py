from selenium.webdriver.chrome.options import Options
from datetime import datetime as dt
from fake_useragent import UserAgent
from selenium import webdriver
from bs4 import BeautifulSoup
import pg_functions as pg
import discord_post as dp
import time
import re

def chrome_driver():
    options = Options()
    # options.add_argument('--headless')
    options.add_argument("window-size=1600,900")
    options.add_argument(f'user-agent={UserAgent().chrome}')
        
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")

    return webdriver.Chrome(options=options)

def get_soup(url):
    driver.get(url)
    time.sleep(1)
    return BeautifulSoup(driver.page_source, 'html.parser')

def check_products(soup, channel, category, subcategory, drops=[]):
    sku_list = soup.find('ol', {'class', 'sku-item-list'}).findAll('li', {'class', 'sku-item'})

    for sku in sku_list:
        title = sku.find('div', {'class', 'sku-title'}).find('a')

        category_dict = {
            'GPU': 1,
            'CPU': 2,
            'Console': 3
        }

        sub_dict = {
            'xbox': 1,
            'ps5': 2,
            'switch': 3,
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

        if re.search("combo", title['href']):
            if sku.find('div', {'class', 'combo-add-to-cart-button'}).find('svg'):
                link = sku.find('div', {'class', 'sku-title'}).find('a')['href']
                id = link[-12:]
                name = title.text.strip()
                price = sku.find('div', {'class', 'priceView-customer-price'}).find('span').text[1:]
                image = 'https://pisces.bbystatic.com/image2/BestBuy_US/Gallery/BestBuy_Logo_2020-190616.png'
                
                dp.discord_webhook_post(channel, subcategory, link, 'Best Buy', name, image)
                time.sleep(1)
                drops.append([id, name, 2, category_dict[category], sub_dict[subcategory], price, link, dt.now().strftime('%Y/%m/%d %H:%M:%S'), '', True])
        else:
            if sku.find('button', {'class', 'add-to-cart-button'}).find('svg'):
                id = sku.find('div', {'class', 'sku-title'}).find('a')['href'][-7:]
                name = title.text.strip()
                price = sku.find('div', {'class', 'priceView-customer-price'}).find('span').text[1:]
                link = f'https://api.bestbuy.com/click/-/{id}/pdp'
                atc = f'https://api.bestbuy.com/click/-/{id}/cart'
                image = f'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/{id[:4]}/{id}_sa.jpg'
                
                dp.discord_webhook_post(channel, subcategory, atc, f'Best Buy - ${price}', name, image)
                time.sleep(1)
                drops.append([id, name, 2, category_dict[category], sub_dict[subcategory], price, link, dt.now().strftime('%Y/%m/%d %H:%M:%S'), atc, False])

    if soup.find('div', {'class', 'footer-category'}).find_next_sibling('div') and not soup.find('a', {'class', 'sku-list-page-next disabled'}):
        driver.get(soup.find('a', {'class', 'sku-list-page-next'})['href'])
        time.sleep(1)
        return check_products(BeautifulSoup(driver.page_source, 'html.parser'), category, subcategory, drops)
    else:
        return drops

def check_product_page(soup, id, category, subcategory, drops=[]):
    if soup.find('button', {'class', 'btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button'}):
        name = soup.find('div', {'class', 'sku-title'}).find('h1').text.strip()
        price = soup.find('div', {'class', 'priceView-customer-price'}).find('span').text[1:]
        link = f'https://api.bestbuy.com/click/-/{id}/pdp'
        atc = f'https://api.bestbuy.com/click/-/{id}/cart'

        drops.append([id, name, 2, category, subcategory, price, link, dt.now().strftime('%Y/%m/%d %H:%M:%S'), atc, False])
    return drops

def check_xbox_consoles(drops):
    xbox_url = 'https://www.bestbuy.com/site/xbox-series-x-and-s/xbox-series-x-and-s-consoles/pcmcat1586900952752.c?id=pcmcat1586900952752'
    return check_products(get_soup(xbox_url), 'xbox', 'Console', 'xbox', drops)

def check_ps5_consoles(drops):
    ps5_url = 'https://www.bestbuy.com/site/playstation-5/ps5-consoles/pcmcat1587395025973.c?id=pcmcat1587395025973'
    return check_products(get_soup(ps5_url), 'ps5', 'Console', 'ps5', drops)

def check_nintendo_switches(drops):
    nintendo_url = 'https://www.bestbuy.com/site/nintendo-switch/nintendo-switch-consoles/pcmcat1484077694025.c?id=pcmcat1484077694025'
    return check_products(get_soup(nintendo_url), 'nintendo', 'Console', 'switch', drops)


def check_rtx_3000_series(drops):
    rtx_dict = {
        '3060': 4,
        '3060 Ti': 5,
        '3070': 6,
        '3080': 7,
        '3090': 8
        }

    rtx_url = 'https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%20{gpu}'

    for gpu in rtx_dict:
        drops = check_products(get_soup(rtx_url.format(gpu=gpu).replace(' ','%20')), 'rtx', 'GPU', gpu.lower().replace(' ',''), drops)
    return drops

def check_radeon_rx_series(drops):
    radeon_dict = {
        '6700 XT': 9,
        '6800 XT': 10,
        '6800': 11,
        '6900 XT': 12
        }

    radeon_url = 'https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~AMD%20Radeon%20RX%20{gpu}'

    for gpu in radeon_dict:
        drops = check_products(get_soup(radeon_url.format(gpu=gpu).replace(' ','%20')), 'radeon', 'GPU', gpu, drops)
    return drops

def check_ryzen_series(drops=[]):
    ryzen_dict = {
        '5600x': ['6438943', 13],
        '5800x': ['6439000', 14],
        '5900x': ['6438942', 15],
        '5950x': ['6438941', 16]
    }

    product_url = 'https://api.bestbuy.com/click/-/{product}/pdp'

    for gpu in ryzen_dict:
        drops = check_product_page(get_soup(product_url.format(product=ryzen_dict[gpu][0])), ryzen_dict[gpu][0], 2, gpu, drops)
        time.sleep(1)
    return drops

def check_all_products(drops=[]):
    drops = check_xbox_consoles(drops)
    drops = check_ps5_consoles(drops)
    drops = check_rtx_3000_series(drops)
    drops = check_radeon_rx_series(drops)
    drops = check_ryzen_series(drops)
    # drops = check_nintendo_switches(drops)
    return drops

driver = chrome_driver()
all_drops = check_all_products()
pg.process_drops(all_drops)
driver.close()