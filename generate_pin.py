import json
import random
import requests
import re
from pathlib import Path

INSTAGRAM_URL = "https://www.instagram.com/rina_vellichor/"

def get_instagram_posts(username="rina_vellichor"):
    """Scrapes Instagram profile and extracts image URLs from all posts."""
    
    url = f"https://www.instagram.com/{username}/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Failed to load Instagram page")

    # Extract sharedData JSON object
    shared_data_match = re.search(r"window\._sharedData = (.*?);</script>", response.text)
    if not shared_data_match:
        raise Exception("Could not extract sharedData")

    shared_data = json.loads(shared_data_match.group(1))
    
    # Navigate the JSON structure
    posts = shared_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]

    image_urls = []
    for post in posts:
        node = post["node"]

        if node["__typename"] == "GraphImage":
            image_urls.append(node["display_url"])

        elif node["__typename"] == "GraphSidecar":
            first_img = node["edge_sidecar_to_children"]["edges"][0]["node"]["display_url"]
            image_urls.append(first_img)

        # skip GraphVideo (we decided no videos)
    
    return image_urls


def load_json_file(filename):
    """Loads JSON list from repository file."""
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    print("Scraping Instagram...")
    posts = get_instagram_posts()

    if not posts:
        raise Exception("No posts found")

    random_image = random.choice(posts)

    titles = load_json_file("titles.json")["titles"]
    descriptions = load_json_file("descriptions.json")["descriptions"]

    random_title = random.choice(titles)
    random_description = random.choice(descriptions)

    output_data = {
        "image_url": random_image,
        "title": random_title,
        "description": random_description,
        "link": "https://rina-vellichor.com/"
    }

    Path("output").mkdir(exist_ok=True)

    with open("output/pin.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print("Generated pin.json")


if __name__ == "__main__":
    main()
