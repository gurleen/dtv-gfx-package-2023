from team_models import Team
from app import DATA_PATH
from typing import Literal
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse
import requests
from bs4 import BeautifulSoup
from os import listdir


HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
}


def ensure_team_dirs(team: Team, gender: Literal["mens", "womens"]):
    team_dir = f"{team.abbreviation.lower()}"
    team_dir_path = Path(DATA_PATH, "headshots", team_dir, gender)
    team_dir_path.mkdir(parents=True, exist_ok=True)
    return str(team_dir_path)


def get_roster_url(team: Team, gender: Literal["mens", "womens"]):
    sport = f"{gender}-basketball"
    url = Path(team.website, "sports", sport, "roster")
    return f"https://{url}"


def try_api_url(base_url: str, gender: Literal["mens", "womens"]):
    url = f"https://{base_url}/api/v2/Rosters/bySport/{gender}-basketball"
    req = requests.get(url, headers=HEADERS)
    if req.status_code == 200:
        return req.json()
    else:
        return None


def remove_query_params(url: str):
    parsed_url = urlparse(url)
    clean_url = urlunparse(parsed_url._replace(query=""))
    return clean_url


def parse_from_html(roster_url: str, base_url: str):
    contents = requests.get(roster_url, headers=HEADERS).text
    soup = BeautifulSoup(contents, "html.parser")
    images = [
        urljoin(f"https://{base_url}", x["data-src"])
        for x in soup.select("div.sidearm-roster-player-image img")
    ]
    images = list(map(remove_query_params, images))
    shirts = [
        x.text.strip() for x in soup.select("span.sidearm-roster-player-jersey-number")
    ]
    return list(zip(shirts, images))


def parse_api_data(data: dict):
    image_urls = list()
    for player in data["players"]:
        shirt = player["jerseyNumber"]
        image = player["image"]["absoluteUrl"]
        image_urls.append((shirt, image))
    return image_urls


def download_images(images: list[tuple[str, str]], folder: str) -> list[str]:
    files = list()
    for shirt, url in images:
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code == 200:
            ext = url.split(".")[-1]
            path = Path(folder, f"{shirt}-raw.{ext}")
            with open(path, "wb") as f:
                f.write(resp.content)
            files.append(str(path))
        else:
            print(f"Error downloading {url}")
    return files

"""
def remove_background(files: list[str], base_dir: str):
    logger.info("Removing backgrounds...")
    interface = HiInterface(
        object_type="object",
        batch_size_seg=5,
        batch_size_matting=1,
        device="cuda" if torch.cuda.is_available() else "cpu",
        seg_mask_size=640,
        matting_mask_size=2048,
        trimap_prob_threshold=250,
        trimap_dilation=30,
        trimap_erosion_iters=3,
        fp16=False,
    )
    processed_images = interface([files[0]])
    logger.info("Backgrounds removed, saving images...")
    for img, fname in zip(processed_images, files):
        name = Path(fname.replace("-raw", "")).with_suffix(".png")
        img.save(name)
    logger.info("Images saved.")
"""

def cache_images_for_team(team: Team, gender: Literal["mens", "womens"]):
    team_dir = ensure_team_dirs(team, gender)

    if listdir(team_dir):
        print(f"Team {team.abbreviation} already has images cached")
        return

    roster_url = get_roster_url(team, gender)
    print(f"Getting images for {team.abbreviation} from {roster_url}")
    if data := try_api_url(team.website, gender):
        images = parse_api_data(data)
    else:
        images = parse_from_html(roster_url, team.website)
    files = download_images(images, team_dir)
    # remove_background(files, team_dir)