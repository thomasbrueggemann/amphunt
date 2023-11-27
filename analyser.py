import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

with open("models.json", "r") as file:
    models = json.load(file)

# Split the "model" property and get the first component
model_names = [model["model"].split()[0] for model in models]

# Calculate the amount of unique first components, which might correlate the brand names
unique_component_estimator = len(set(model_names))

# Extract the model names
model_names = [model["model"] for model in models]

# Vectorize the model names
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(model_names)

# Perform clustering
print(f"Clustering with {unique_component_estimator} clusters")
kmeans = KMeans(n_clusters=unique_component_estimator)  # Change the number of clusters as needed
kmeans.fit(X)

# Get the cluster labels
cluster_labels = kmeans.labels_

# Print the clusters
clustered_models = {}
for i in range(len(models)):
    cluster_label = int(cluster_labels[i])
    
    if cluster_label not in clustered_models:
        clustered_models[cluster_label] = []
    
    clustered_models[cluster_label].append(models[i])

# Write clustered_models to a JSON file
with open("clustered_models.json", "w") as file:
    json.dump(clustered_models, file, indent=4)






