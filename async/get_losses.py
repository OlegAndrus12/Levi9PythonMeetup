import re
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
from datetime import datetime
import requests
from time import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from threading import Thread

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.1)
adapter = HTTPAdapter(max_retries=retry)
session.mount("http://", adapter)
session.mount("https://", adapter)


def parse(url):
    response = session.get(url)
    result = {}
    response = response.text
    result = list()
    soup = BeautifulSoup(response, "html.parser")
    res = soup.select("ul[class=see-also] li[class=gold]")
    for element in res:
        losses = element.select("div[class=casualties] div ul li")
        for l in losses:
            title, quantity, *rest = " ".join(l.text).split("—")
            title = re.sub("\s", "", title.strip())
            quantity = re.search(r"\d+", quantity).group()
            result.append({title: int(quantity)})
    return response.status_code


def parse_pages(urls):
    for url in urls:
        yield parse(url)


def main(pages):
    result = list()
    for page in pages:
        result.append(page)
    return result


if __name__ == "__main__":
    with open("links.json", "r") as f:
        urls = json.loads(f.readline())
    start_time = time()
    res = main(parse_pages(urls*20))
    elapsed_time = time() - start_time
    print("\nSync completed in {} seconds".format(elapsed_time))

    # with open("losses.json", "w") as f:
    #     f.writelines(json.dumps(res, ensure_ascii=False))
