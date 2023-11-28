import json
from fuzzywuzzy import fuzz
from tqdm import tqdm

with open("models.json", "r") as file:
    models = json.load(file)

with open("brands.json", "r") as file:
    brands = json.load(file)

with tqdm(total=len(models), desc="Processing models") as pbar:
    for model in models:
        model_name = model["model"]
        for brand in brands:
            similarity_ratio = fuzz.token_set_ratio(model_name, brand)
            if similarity_ratio >= 80:  # Adjust the threshold as needed

                if not "brands" in model:
                    model["brands"] = []

                model["brands"].append(brand)

        pbar.update(1)

count = sum("brands" not in model for model in models)
print(f"{count} models without brands")
print()

with open("model_brands.json", "w") as file:
    json.dump(models, file, indent=4)

brands_dict = {}

for model in models:
    if "brands" in model:
        for brand in model["brands"]:
            if brand not in brands_dict:
                brands_dict[brand] = []
            
            brands_dict[brand].append(model)

sorted_brands = sorted(brands_dict, key=lambda x: len(brands_dict[x]), reverse=True)
for brand in sorted_brands:
    count = len(brands_dict[brand])
    print(f"{brand}: {count}")

with open("brand_models.json", "w") as file:
    json.dump(brands_dict, file, indent=4)

