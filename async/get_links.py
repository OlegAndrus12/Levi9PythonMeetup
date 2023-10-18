import re
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import requests

BASE_URL = "https://index.minfin.com.ua/ua/russian-invading/casualties"


def get_links():
    response = requests.get(BASE_URL)
    data = response.text
    soup = BeautifulSoup(data, "html.parser")
    content = soup.select("div[class=ajaxmonth] h4[class=normal] a")
    urls = [BASE_URL]
    prefix = BASE_URL + "/month.php?month="
    for tag_a in content:
        urls.append(prefix + re.search(r"\d{4}-\d{2}", tag_a["href"]).group())
    return urls


if __name__ == "__main__":
    res = get_links()
    with open("links.json", mode="w") as f:
        f.writelines(json.dumps(res))
    print(res)
