# coding: utf8

# TODO: make docker container with autodownload geckodriver and autoinstalling selenium and BeautifulSoup
import sys
from collections import OrderedDict
from pprint import pprint
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver


ELEMEENTAREE_LINK_PREFIX = "https://elementaree.ru/menu/?category=3.1&payment=recurrent&period="
ELEMEENTAREE_LINK_SUFFIX = "&types_of_dishes=main_dishes_new.main_dishes_hit.soups.salads.breakfasts.snacks.fruit"


def get_setup_browser_driver():
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('permissions.default.image', 2)
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    browser = webdriver.Firefox(firefox_profile=firefox_profile)
    browser.implicitly_wait(10)
    return browser


def get_elementaree_link(week_start_date_str):
    return ELEMEENTAREE_LINK_PREFIX + week_start_date_str + ELEMEENTAREE_LINK_SUFFIX


def get_menu(generated_html):
    soup = BeautifulSoup(generated_html, 'lxml')
    dish_set = set()
    lines = []
    for tag in soup.find_all("div"):
        if "Цена за" in tag.text and len(tag.text) < 200 and not tag.text[0].isdigit() and tag.text not in dish_set:
            lines.append(tag.text)
            dish_set.add(tag.text)
    dish_name_to_href = {}
    for tag in soup.find_all("a"):
        dish_name_to_href[tag.text] = tag.get('href')
    dish_line_to_href = {}
    for l in dish_set:
        for ll in dish_name_to_href.keys():
            if l.startswith(ll):
                dish_line_to_href[l] = dish_name_to_href[ll]
    for l in lines:
        print(l)
    index = None
    for i, line in enumerate(lines):
        if 'суп ' in line.lower() or ' суп' in line.lower():
            index = i
            break
    lines = lines[:index]
    for l in lines:
        print(l)

    dish_name_to_href2 = OrderedDict()
    for i, line in enumerate(lines):
        print('i', i)
        for dish_name in dish_name_to_href.keys():
            if dish_name and line.startswith(dish_name):
                dish_href = dish_line_to_href[line]

                print ('dish_name', dish_name)
                print('link', dish_href)
                print()
                dish_name_to_href2[dish_name] = dish_href

    return dish_name_to_href2


def get_dish_info(dish_name, dish_href):
    short_list = []
    print('dish_name', dish_name)
    print('link', dish_href)
    print()
    browser.implicitly_wait(10)
    browser.get(dish_href)
    sleep(3)
    generated_html = browser.page_source
    soup = BeautifulSoup(generated_html, 'lxml')
    for tag in soup.find_all():
        x = tag.text
        if x.lower()[:10].startswith(
                dish_name.lower()[:10]) and 'можно приготовить' in x.lower() and 'минут' in x.lower():
            short_list.append(x)
    pprint(short_list)
    if not short_list:
        for tag in soup.find_all():
            x = tag.text
            if 'можно приготовить' in x.lower() or 'минут' in x.lower():
                print(x)
    dish_description = sorted(short_list, key=lambda x: len(x), reverse=True)[0]
    fixed_line = dish_description\
        .lower()\
        .replace('\xa0', ' ')\
        .replace('день', 'день\n')\
        .replace('минут', 'минут\n')\
        .replace('добавить в корзину', '\n')\
        .replace('что в наборе', 'что в наборе\n')\
        .replace('на 100 г блюда', '\n')\
        .replace('можно приготовить на ', '\n')
    splitted_fixed_line = fixed_line.split('\n')
    day = splitted_fixed_line[1][:2].strip()
    minutes = splitted_fixed_line[2][:2].strip()
    ingredients = splitted_fixed_line[5].strip()
    price = splitted_fixed_line[3][:4].strip()
    print(fixed_line)
    return OrderedDict(
        {'dish_name': dish_name,
         'day': day,
         'price': price,
         'minutes': minutes,
         'ingredients': ingredients})


def process_all_dishes(dish_name_to_href):
    dish_info_list = []
    for i, dish in enumerate(dish_name_to_href.items()):
        dish_name = dish[0]
        dish_href = dish[1]
        print('i', i)
        dish_info = get_dish_info(dish_name, dish_href)
        dish_info_list.append(dish_info)
        print(dish_info)
        print()

    return dish_info_list


def dump_dish_info_list_to_file(dish_info_list, filename):
    table_header = ['блюдо', 'день', 'цена', 'время', 'состав']
    header = '\t'.join(table_header)
    table_lines = list(sorted(dish_info_list, key=lambda x: (int(x['day']), int(x['price']))))
    table_lines = ['\t'.join(x.values()) for x in table_lines]
    final_table = '\n'.join([header] + table_lines)
    open(filename, 'w').write(final_table)


if __name__ == '__main__':
    week_start_date_str = sys.argv[-1]
    browser = get_setup_browser_driver()
    elementaree_link = get_elementaree_link(week_start_date_str)

    print(sys.argv[-1])
    print(elementaree_link)

    browser.get(elementaree_link)
    sleep(5)

    dish_name_to_href = get_menu(browser.page_source)

    dish_info_list = process_all_dishes(dish_name_to_href)
    filename = sys.argv[-1] + '.tsv'
    dump_dish_info_list_to_file(dish_info_list, filename)
