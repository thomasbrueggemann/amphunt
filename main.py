import requests
from bs4 import BeautifulSoup
import re
import json
from tqdm import tqdm
import os
import csv

base_url = "https://tonehunt.org"
page = 0
has_more_pages = True
detail_links = []

while has_more_pages:
    url = f"{base_url}/all?sortDirection=desc&filter=amp&page={page}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    anchor_tags = soup.find_all("a", href=re.compile(r"/\w{8}-\w{4}-\w{4}-\w{4}-\w{12}"))
    
    new_links = [tag["href"] for tag in anchor_tags]
    detail_links.extend(new_links)
    
    has_more_pages = len(new_links) > 0
    page += 1
    print(f"Page {page} scraped, {len(new_links)} links found, {len(detail_links)} total...")

models_filepath = "models.json"
if os.path.exists(models_filepath):
    with open("models.json", "r") as json_file:
        models = json.load(json_file)
else:
    models = []

try:
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

        form = soup.find("form", action="/favorites/add")
        if form:
            favs_text = re.sub(r'\D', '', form.text)
            model["favs"] = int(favs_text)

            buttom = form.find_next_sibling("button")
            if buttom:
                downloads_text = re.sub(r'\D', '', buttom.text)
                model["downloads"] = int(downloads_text)

        models.append(model)

except Exception as e:
    print(e)

finally:
    with open("models.json", "w") as json_file:
        json.dump(models, json_file, indent=4)

    with open("models.csv", "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["id", "model", "favs", "downloads", "url"], delimiter=";")
        writer.writeheader()
        writer.writerows(models)
