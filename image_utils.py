import requests
import os
import shutil


HEADERS = {
    "User-Agent": "AnimalImageFetcher/1.0 (your_email@example.com)"
}

WIKI_API = "https://en.wikipedia.org/w/api.php"

LOCAL_IMAGE_MAP = {     #local manually added images
    "Blobfish": "static/images/Blobfish.jpeg",
    "Fossa": "static/images/fossa.jpeg",
    "Kiwi": "static/images/kiwi.jpeg",
    "Red-Eyed Tree Frog": "static/images/red-eye tree frog.jpeg",
    "Amazon Rainforest Frog": "static/images/Amz rainforest frog.jpeg",
    "Titanoboa": "static/images/titanoboa.jpeg",
    "Woolly Mammoth": "static/images/woolly mammoth.jpeg",
    "Shoots": "static/images/shoots.jpeg",
    "Stems": "static/images/stems.jpeg",
    "Bark": "static/images/bark.jpeg",
    "Clam": "static/images/clam.jpeg",
    "Seal": "static/images/seal.jpeg",
    "Pangolin": "static/images/pangolin.jpeg",
    "Blue Morpho Butterfly": "static/images/Blue Morpho Butterfly.jpeg",
    "Monitor Lizard": "static/images/monitor-lizard.jpeg"
}

def resolve_title(animal_name):     #uses full search engine (searches multiple articles)
    params = {
        "action": "query",
        "list": "search",
        "srsearch": animal_name,
        "format": "json"
    }

    r = requests.get(WIKI_API, params=params, headers=HEADERS)
    r.raise_for_status()
    results = r.json().get("query", {}).get("search", [])

    #return top ranked page in wiki
    return results[0]["title"] if results else None


def get_animal_image(animal_name):
    
    #check if it's manually added
    for name, path in LOCAL_IMAGE_MAP.items():
        if name.lower() == animal_name.lower():
            if os.path.exists(path):
                return path
            else:
                print(f"Missing local image file: {path}")
    
    #look for image directly
    params = {
        "action": "query",
        "titles": animal_name,
        "prop": "pageimages",
        "format": "json",
        "pithumbsize": 1000,
        "redirects": 1      #allows page redirect
    }

    r = requests.get(WIKI_API, params=params, headers=HEADERS)
    r.raise_for_status()
    page = next(iter(r.json()["query"]["pages"].values()))

    if "thumbnail" in page:
        return page["thumbnail"]["source"]

    # Search fallback
    resolved = resolve_title(animal_name)       #try another page
    if not resolved:
        return None

    params["titles"] = resolved     #get image from other page
    r = requests.get(WIKI_API, params=params, headers=HEADERS)
    r.raise_for_status()
    page = next(iter(r.json()["query"]["pages"].values()))

    return page.get("thumbnail", {}).get("source")

def download_image(image_source, filename):
    if not image_source:
        return

    # Wikipedia / remote image
    if image_source.startswith("http"):
        response = requests.get(image_source, headers=HEADERS)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)

    # Local image path
    else:
        if os.path.exists(image_source):
            shutil.copy(image_source, filename)
        else:
            print(f"Local image not found: {image_source}")