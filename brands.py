
import requests
import json

from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

def parse_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'
    }
    response = requests.get(url, headers=headers)
    html = response.text

    return BeautifulSoup(html, 'html.parser')

print('Scraping brands from Andertons ...')

andertons_html = parse_html('https://www.andertons.co.uk/brands')
andertons_brands = [tag.text.strip() for tag in andertons_html.find_all('a', class_='brand-list__brand-link')]

print('Scraping brands from Thomann ...')

thomann_html = parse_html('https://www.thomann.de/de/cat_brands.html?catKey=gi')
thomann_brands = [tag.text.strip() for tag in thomann_html.find_all('a', class_='fx-brand-list__item')]

print('Scraping brands from Sweetwater ...')

sweetwater_html = parse_html('https://www.sweetwater.com/store/manufacturer/guitar')
sweetwater_brands = [tag.text.strip() for tag in sweetwater_html.find('div', id='manuList').find_all('a')]

print('Scraping brands from TubeTechnic ...')
tubetechnic_html = parse_html('https://tubetechnic.com/list-of-boutique-amp-makers/')
tubetechnic_content = tubetechnic_html.find('div', id='content').text
tubetechnic_brands = [line.strip() for line in tubetechnic_content.split('\n') if line.strip() != '']

brands = list(set(andertons_brands + thomann_brands + sweetwater_brands + tubetechnic_brands))

words = []
for brand in brands:
    words.extend(brand.split())



brands_expanded = [{'original_name': brand, 'lowercase_name': brand.lower()} for brand in brands]
unique_lowercase_brands = {brand['lowercase_name']: brand for brand in brands_expanded}.values()

unique_brands = [brand['original_name'] for brand in unique_lowercase_brands]

# Remove duplicates based on text similarity
unique_brands_filtered = []
for brand in unique_brands:
    is_duplicate = False
    for filtered_brand in unique_brands_filtered:
        similarity = fuzz.ratio(brand, filtered_brand)
        if similarity > 80:  # Adjust the similarity threshold as needed
            is_duplicate = True
            if len(brand) < len(filtered_brand):
                filtered_brand = brand
            break
    if not is_duplicate:
        unique_brands_filtered.append(brand)

unique_brands_filtered.sort()

with open('brands.json', 'w') as file:
    json.dump(unique_brands_filtered, file, indent=4)
