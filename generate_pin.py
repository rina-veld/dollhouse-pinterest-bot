import os
import json
import random
from pathlib import Path

GITHUB_USER = "rina-veld"  # ← замени на своё имя пользователя на GitHub, если другое
REPO_NAME = "dollhouse-pinterest-bot"
BRANCH = "main"

def get_random_image():
    """Returns a random image file name from the images folder."""
    images_path = Path("images")
    if not images_path.exists():
        raise Exception("images/ folder not found")

    files = [f for f in images_path.iterdir() if f.is_file()]

    if not files:
        raise Exception("No files in images/ folder")

    random_file = random.choice(files)
    return random_file.name


def load_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    print("Selecting random image...")

    # pick a random image name
    image_file = get_random_image()

    # build RAW github URL
    image_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/images/{image_file}"

    print("Random image:", image_url)

    # load titles & descriptions
    titles = load_json("titles.json")["titles"]
    descriptions = load_json("descriptions.json")["descriptions"]

    random_title = random.choice(titles)
    random_description = random.choice(descriptions)

    output_data = {
        "image_url": image_url,
        "title": random_title,
        "description": random_description,
        "link": "https://rina-vellichor.com/"
    }

    Path("output").mkdir(exist_ok=True)

    with open("output/pin.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print("✔ pin.json created successfully")


if __name__ == "__main__":
    main()
