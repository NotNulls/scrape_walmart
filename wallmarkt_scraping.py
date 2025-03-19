import requests
from bs4 import BeautifulSoup

walmart_ur = "https://www.walmart.com/ip/LG-27-Color-Smart-Green-27SR50F-G-AUS/5465289649?adsRedirect=true"

HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "accept": "application/json",
    "accept-language": "en-US",
    "accept-encoding": "gzip, deflate, br, zstd",
}

response = requests.get(walmart_ur, headers=HEADERS)

soup = BeautifulSoup(response.text, "html.parser")
script_tag = soup.find("script", id="__NEXT_DATA__")

html = script_tag

print(html)