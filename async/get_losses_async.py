import aiohttp
import asyncio
import re
import json
from time import time
from bs4 import BeautifulSoup


async def parse_page(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response = await response.text()
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

            return result


async def parse_pages(urls):
    for url in urls:
        yield parse_page(url)


async def main(pages):
    result = list()
    async for page in pages:
        result.append(page)
    return await asyncio.gather(*result)


if __name__ == "__main__":
    with open("links.json", "r") as f:
        urls = json.loads(f.readline())

    start_time = time()
    res = asyncio.run(main(parse_pages(urls)))
    elapsed_time = time() - start_time
    print("All tasks completed in {} seconds".format(elapsed_time))
