
import chevron
import json
import re
import datetime

def slugify(text):
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[\s_]+", "-", text)
    return text

def render_brand_page(brand, brand_models):
    id = slugify(brand)

    brand_models.sort(key=lambda x: x.get("downloads", 0), reverse=True)

    with open('detail.mustache', 'r') as f:
        result = chevron.render(f, {
            'brand': brand,
            'models': brand_models,
            'last_updated': datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M") + " UTC"
        })

    with open(f'docs/{id}.html', 'w') as f:
        f.write(result)

with open('brand_models.json', 'r') as f:
    data = json.load(f)

brands = {key: len(value) for key, value in data.items()}
brands = dict(sorted(brands.items(), key=lambda x: x[1], reverse=True))
brands_list = [{'brand': key, 'id': slugify(key), 'count': value} for key, value in brands.items()]

# generate index page
with open('index.mustache', 'r') as f:
    result = chevron.render(f, {
        'brands': brands_list,
        'last_updated': datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M") + " UTC"
    })

with open('docs/index.html', 'w') as f:
    f.write(result)

# generate detail pages
for brand, models in data.items():
    render_brand_page(brand, models)