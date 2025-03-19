import requests
from bs4 import BeautifulSoup
import json

HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "accept": "application/json",
    "accept-language": "en-US",
    "accept-encoding": "gzip, deflate, br, zstd",
}

site_url = "https://www.walmart.com"


def get_product_lnk(query, page_num=1):
    search_template_url = f"https://www.walmart.com/search?q={query}&page={page_num}"
    response = requests.get(search_template_url, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all('a', href=True)

    product_links = []

    for a_tag in links:
        if '/ip/' in a_tag['href']:
            found = True
            if "https" in a_tag['href']:
                complete_url = a_tag['href']
                product_links.append(complete_url)
            else:
                complete_url = site_url + a_tag['href']
                product_links.append(complete_url)
            if not found:
                print("\n\nSoup not found", soup)

    return product_links


def extract_prod_info(product_url):
    response = requests.get(product_url, headers=HEADERS)

    # use web token counter to find the value for the price or import json lib
    soup = BeautifulSoup(response.text, "html.parser")
    script_tag = soup.find("script", id="__NEXT_DATA__")

    if script_tag is None:
        return None

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

    return product_info


def main():
    output_file = "p_info.json"
    with open(output_file, "w") as file:
        page_num = 1
        while True:
            links = get_product_lnk("monitors", page_num)
            if not links or page_num > 1:
                break

            for link in links:
                try:
                    product_info = extract_prod_info(link)
                    if product_info:
                        file.write(json.dumps(product_info)+"\n")
                except Exception as e:
                    print(f"Process failed for URL: {link}. \n Error: {e}")
            page_num += 1
            print(f"Searched page {page_num}")



if __name__ == "__main__":
    main()
