
import requests
import re
import json

from tqdm import tqdm
from bs4 import BeautifulSoup

base_url = "https://tonehunt.org"
page = 0
has_more_pages = True
detail_links = []

while has_more_pages:
    url = f"{base_url}/models?layout=list&sortDirection=desc&filter=amp&page={page}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    anchor_tags = soup.find_all("a", href=re.compile(r"/\w{8}-\w{4}-\w{4}-\w{4}-\w{12}"))
    
    new_links = [tag["href"] for tag in anchor_tags]
    detail_links.extend(new_links)
    
    has_more_pages = len(new_links) > 0
    page += 1
    print(f"Page {page} scraped, {len(new_links)} links found, {len(detail_links)} total...")

models = []

progress_bar = tqdm(detail_links, desc="Scraping pages", unit="pages")
for link in progress_bar:

    id = link.split("/")[-1]

    if any(m["id"] == id for m in models):
        continue    

    url = f"{base_url}{link}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    model = {
        "id": id,
        "url": url,
        "favs": 0,
        "downloads": 0
    }

    make_and_model_h5 = soup.find("h5", string="Make and model")
    if make_and_model_h5:
        model_h4 = make_and_model_h5.find_next_sibling("h4")
        if model_h4:
            model["model"] = model_h4.text

    headers = soup.find_all("header")
    for header in headers:
        first_h3 = header.find("h3")
        if first_h3:
            model["title"] = first_h3.text
            break

    form = soup.find("form", action="/favorites/add")
    if form:
        favs_text = re.sub(r'\D', '', form.text)
        model["favs"] = int(favs_text)

        buttom = form.find_next_sibling("button")
        if buttom:
            downloads_text = re.sub(r'\D', '', buttom.text)
            model["downloads"] = int(downloads_text)

    models.append(model)

with open("models.json", "w") as json_file:
    json.dump(models, json_file, indent=4)
