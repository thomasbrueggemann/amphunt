import requests
from bs4 import BeautifulSoup
import json

url = "https://www.andertons.co.uk/brands"
response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, 'html.parser')

anchor_tags = soup.find_all('a', class_='c-all-brands-desktop__link')
anchor_texts = [tag.text for tag in anchor_tags]

with open('brands.json', 'w') as file:
    json.dump(anchor_texts, file, indent=4)



