import requests
from bs4 import BeautifulSoup
import json

walmart_ur = "https://www.walmart.com/ip/LG-27-Color-Smart-Green-27SR50F-G-AUS/5465289649?adsRedirect=true"

HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "accept": "application/json",
    "accept-language": "en-US",
    "accept-encoding": "gzip, deflate, br, zstd",
}


def extract_prod_info(product_url):
    response = requests.get(product_url, headers=HEADERS)

    #use web token counter to find the value for the price or import json lib
    soup = BeautifulSoup(response.text, "html.parser")
    script_tag = soup.find("script", id="__NEXT_DATA__")

    data = json.loads(script_tag.string)
    initial_data = data["props"]["pageProps"]["initialData"]["data"]
    product_data = initial_data["product"]
    reviews_data = initial_data.get("reviews", {})


    product_info = {
                    "price": product_data["priceInfo"]["currentPrice"]["price"],
                    "review_count": reviews_data.get("totalReviewCount", 0),
                    "item_id": product_data["usItemId"],
                    "avg_rating": reviews_data.get("averageOverallRating", 0),
                    "product_name": product_data["name"],
                    "brand": product_data.get("brand", ""),
                    "availability": product_data["availabilityStatus"],
                    "image_url": product_data["imageInfo"]["thumbnailUrl"],
                    "short_description": product_data.get("shortDescription", "")
                }

    #html = script_tag

    return product_info