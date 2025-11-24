import json
import random
import requests
from pathlib import Path

USERNAME = "rina_vellichor"
PROFILE_API = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={USERNAME}"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*"
}

def get_instagram_posts():
    """Fetch posts from Instagram using the public API endpoint."""
    response = requests.get(PROFILE_API, headers=HEADERS)

    if response.status_code != 200:
        raise Exception(f"Instagram API error: {response.status_code}")

    data = response.json()

    posts = data["data"]["user"]["edge_owner_to_timeline_media"]["edges"]

    images = []

    for item in posts:
        node = item["node"]

        if node["__typename"] == "GraphImage":
            images.append(node["display_url"])

        elif node["__typename"] == "GraphSidecar":
            first = node["edge_sidecar_to_children"]["edges"][0]["node"]["display_url"]
            images.append(first)

        # skip videos

    return images


def load_json_list(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    print("Fetching Instagram posts...")
    posts = get_instagram_posts()

    if not posts:
        raise Exception("No posts found")

    random_image = random.choice(posts)

    titles = load_json_list("titles.json")["titles"]
    descriptions = load_json_list("descriptions.json")["descriptions"]

    random_title = random.choice(titles)
    random_description = random.choice(descriptions)

    output = {
        "image_url": random_image,
        "title": random_title,
        "description": random_description,
        "link": "https://rina-vellichor.com/"
    }

    Path("output").mkdir(exist_ok=True)

    with open("output/pin.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)

    print("✔ pin.json generated!")


if __name__ == "__main__":
    main()
