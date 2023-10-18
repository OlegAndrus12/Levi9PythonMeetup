import aiohttp
import re
from bs4 import BeautifulSoup
import asyncio
import json

BASE_URL = "https://index.minfin.com.ua/ua/russian-invading/casualties"


async def get_links():
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL) as response:
            response = await response.text()
            soup = BeautifulSoup(response, "html.parser")
            content = soup.select("div[class=ajaxmonth] h4[class=normal] a")
            urls = ["/"]
            prefix = BASE_URL + "/month.php?month="
            for tag_a in content:
                urls.append(prefix + re.search(r"\d{4}-\d{2}", tag_a["href"]).group())
            return urls


if __name__ == "__main__":
    res = asyncio.run(get_links())
    with open("links.json", mode="w") as f:
        f.writelines(json.dumps(res))
    print(res)
