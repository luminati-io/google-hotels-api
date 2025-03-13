# Google Hotels Scraper

Learn how to scrape real-time hotel data from Google – one of the largest travel data aggregators. We cover two methods:

1. **Free Scraper**: Ideal for small-scale needs.
2. **Bright Data Google Hotels API**: An enterprise-grade solution for collecting public Google Hotels data at scale with a single API call (part of the [SERP Scraping API](https://brightdata.com/products/serp-api)).


## Table of Contents
- [Free Scraper](#free-scraper)
  - [Setup](#setup)
  - [Usage](#usage)
  - [Sample Output](#sample-output)
  - [Limitations](#limitations)
- [Bright Data Google Hotels API](#bright-data-google-hotels-api)
  - [Key Features](#key-features)
  - [Prerequisites](#prerequisites)
  - [Direct API Access](#direct-api-access)
  - [Native Proxy-Based Access](#native-proxy-based-access)
- [Advanced Features](#advanced-features)
  - [Localization Parameters](#localization-parameters)
  - [Booking Parameters](#booking-parameters)
  - [Device Type Parameters](#device-type-parameters)
  - [Response Format](#response-format)
- [Alternative Solutions](#alternative-solutions)
- [Support & Resources](#support--resources)

## Free Scraper

A quick-and-easy scraper for extracting Google Hotels data on a smaller scale.

<img width="800" alt="free-google-hotels-scraper" src="https://github.com/luminati-io/google-hotels-api/blob/main/images/421713152-9e86aabe-c8b7-4286-946a-378cd98c81b3.png" />

### Setup

**Requirements:**

- [Python 3.9+](https://www.python.org/downloads/)
- [Selenium](https://pypi.org/project/selenium/) for browser automation
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) for parsing HTML
- Other helper libraries like `pandas`, `tqdm`, `webdriver-manager`

**Installation:**

```bash
pip install pandas tqdm selenium beautifulsoup4 webdriver-manager
```

**Note**: If you're new to web scraping, we recommend starting with our [Python web scraping for beginners tutorial](https://brightdata.com/blog/how-tos/web-scraping-with-python) or our [Guide to Web Scraping With Selenium](https://brightdata.com/blog/how-tos/using-selenium-for-web-scraping).

### **Usage**
Run the [google-hotels-scraper.py](https://github.com/luminati-io/Google-Hotels-Scraper/blob/main/google-hotels-scraper/google-hotels-scraper.py) script with the required parameters:
```bash
python3 google-hotels-scraper.py --location "Dubai" --max_hotels 200
```
_Parameters:_
- `location` – the target location for hotel data
- `max_hotels` – the number of hotels to scrape

💡 **Pro Tip:** Comment out the line `options.add_argument("--headless=new")` in the script to reduce detection by Google's anti-scraping systems.

### Sample Output
<img width="800" alt="google-hotels-scraper-csv-output" src="https://github.com/luminati-io/google-hotels-api/blob/main/images/421731827-633afbf9-204e-444a-ac0f-23b8b72c5813.png" />


### Limitations

The Free Scraper has several constraints:

- High risk of IP blocks
- Limited request volume
- Frequent CAPTCHAs
- Unreliable for large-scale scraping

Consider Bright Data's dedicated solution below for larger and more reliable data collection 👇


## Bright Data Google Hotels API
[Bright Data's Google Hotels API](https://brightdata.com/products/serp-api/google-search/hotels) is part of the [SERP Scraping API](https://brightdata.com/products/serp-api) and uses our advanced [proxy network](https://brightdata.com/proxy-types). It helps you collect public Google Hotels data at scale – without worrying about CAPTCHA or IP blocks.

### Key Features
- **Global Location Accuracy**: Tailor results to specific locations
- **Pay-Per-Success Model**: Only pay for successful requests
- **Real-Time Data**: Get up-to-date hotel information in seconds
- **Scalability**: Handle unlimited requests with no volume restrictions
- **Cost Efficiency**: Save on infrastructure and maintenance costs
- **High Reliability**: Consistent performance with built-in anti-blocking measures
- **24/7 Support**: Expert help whenever you need it


### Prerequisites

1. Create a [Bright Data account](https://brightdata.com/) (new users get $5 credit)
2. Generate your [API key](https://docs.brightdata.com/general/account/api-token)
3. Follow our [step-by-step guide](https://github.com/luminati-io/Google-Hotels-Scraper/blob/main/setup-serp-api-guide.md) to configure the SERP API and access credentials
4. To use the Google Hotels API, you'll need the entity ID of the hotel you want to query. You can find this by:
	1. Searching for the hotel name in Google
	2. Right-clicking and selecting "View page source"
	3. Searching for "/entity" on the page to find the entity ID

### Direct API Access

Make a direct request to the API endpoint.

**cURL Example:**

```bash
curl https://api.brightdata.com/request \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer API_TOKEN" \
  -d '{
        "zone": "ZONE_NAME",
        "url": "https://www.google.com/travel/hotels/entity/CgoIyNaqqL33x5ovEAE/prices?brd_json=1",
        "format": "raw"
      }'
```

**Python Example:**

```python
import requests
import json

url = "https://api.brightdata.com/request"
headers = {"Content-Type": "application/json", "Authorization": "Bearer API_TOKEN"}

payload = {
    "zone": "ZONE_NAME",
    "url": "https://www.google.com/travel/hotels/entity/CgoIyNaqqL33x5ovEAE/prices?brd_json=1",
    "format": "raw",
}

response = requests.post(url, headers=headers, json=payload)

with open("serp-direct-api.json", "w") as file:
    json.dump(response.json(), file, indent=4)

print("Response saved to 'serp-direct-api.json'.")
```

👉 See the [full JSON output](https://github.com/luminati-io/Google-Hotels-Scraper/blob/main/google-hotels-api-results/serp-direct-api.json).

**Note:** Use `brd_json=1` for parsed JSON or `brd_json=html` for parsed JSON + full nested HTML.

### Native Proxy-Based Access

You can also use Bright Data's proxy routing method:

**cURL Example:**

```bash
curl -i \
  --proxy brd.superproxy.io:33335 \
  --proxy-user "brd-customer-<customer-id>-zone-<zone-name>:<zone-password>" \
  -k \
  "https://www.google.com/travel/hotels/entity/CgoIyNaqqL33x5ovEAE/prices?brd_json=html"
```

**Python Example:**

```python
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

host = "brd.superproxy.io"
port = 33335
username = "brd-customer-<customer-id>-zone-<zone-name>"
password = "<zone-password>"
proxy_url = f"http://{username}:{password}@{host}:{port}"

proxies = {"http": proxy_url, "https": proxy_url}
url = "https://www.google.com/travel/hotels/entity/CgoIyNaqqL33x5ovEAE/prices?brd_json=html"
response = requests.get(url, proxies=proxies, verify=False)

with open("serp-native-proxy.html", "w", encoding="utf-8") as file:
    file.write(response.text)

print("Response saved to 'serp-native-proxy.html'.")
```

👉 See the [full JSON output](https://github.com/luminati-io/Google-Hotels-API/blob/main/google-hotels-api-results/serp-native-proxy.html).

**Note:** For production environments, load Bright Data's SSL certificate as described in the [SSL Certificate Guide](https://docs.brightdata.com/general/account/ssl-certificate).

## Advanced Features

Bright Data's API supports many advanced parameters for fine-tuning your Google Hotels data extraction. Below are examples using **Native Proxy-Based Access**, but you can apply them via Direct API Access as well.

### Localization Parameters

<img width="800" alt="bright-data-google-hotels-scraper-api-localization" src="https://github.com/luminati-io/google-hotels-api/blob/main/images/422299775-d47254c1-0c7f-4572-bf54-f3f55cf66908.png" />


These parameters define the country and language of the search:

| Parameter | Description | Example |
| --- | --- | --- |
| gl | Two-letter country code | `gl=us` (United States) |
| hl | Two-letter language code | `hl=en` (English) |

**Example:** Search for hotels in the United States with results in English:

```bash
curl --proxy brd.superproxy.io:33335 --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
"https://www.google.com/travel/hotels/entity/CgoI4NzJmsPmkpU6EAE/prices?gl=us&hl=en"
```

### Booking Parameters

<img width="800" alt="bright-data-google-hotels-scraper-api-booking-params" src="https://github.com/luminati-io/google-hotels-api/blob/main/images/422303757-74faadf7-218b-4fa3-b2d9-d0cecf8e23e6.png" />

These parameters help refine results based on dates, number of guests, free cancellation, and accommodation type:

| Parameter | Description | Format | Example |
|-----------|-------------|--------|---------|
| brd_dates | Check-in and check-out dates | YYYY-MM-DD,YYYY-MM-DD | `brd_dates=2025-08-15,2025-08-20` |
| brd_occupancy | Number of guests (adults + children) | `<adults>,<child1_age>,<child2_age>` | `brd_occupancy=3,6,9` (3 adults, 2 children aged 6 & 9) |
| brd_free_cancellation | Only show refundable bookings | true or false | `brd_free_cancellation=true` |
| brd_accomodation_type | Type of stay | hotels or vacation_rentals | `brd_accomodation_type=vacation_rentals` |
| brd_currency | Currency for displaying prices | 3-letter currency code | `brd_currency=GBP` (British Pounds) |


**Example:** Search for a hotel stay with specific parameters:
```bash
curl --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://www.google.com/travel/hotels/entity/CgoIyNaqqL33x5ovEAE/prices\
?brd_dates=2025-04-15,2025-04-20\
&brd_occupancy=3,6,9\
&brd_free_cancellation=true\
&brd_currency=GBP"
```


### Device Type Parameters
By default, requests mimic a desktop user-agent, but you can change it to mobile:

| Parameter | Description | 
|-----------|-------------|
| `brd_mobile=0` | Random desktop user-agent (default) | 
| `brd_mobile=1` | Random mobile user-agent |
| `brd_mobile=ios` | iPhone user-agent |
| `brd_mobile=android` | Android phone user-agent |
| `brd_mobile=ipad` | iPad user-agent |
| `brd_mobile=android_tablet` | Android tablet user-agent |

**Example:** Fetch hotel data with an Android phone user-agent:

```bash
curl --proxy brd.superproxy.io:33335 --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
"https://www.google.com/travel/hotels/entity/CgoIyNaqqL33x5ovEAE/prices?brd_mobile=android"
```

### Response Format
By default, responses are in HTML, but you can request a JSON response:

| Parameter | Description |
|-----------|-------------|
| `brd_json=1` | Returns JSON response instead of HTML |
| `brd_json=html`	| JSON + full nested HTML |

**Example:** Get hotel price data in JSON format:

```bash
curl --proxy brd.superproxy.io:33335 --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
"https://www.google.com/travel/hotels/entity/CgoIyNaqqL33x5ovEAE/prices?brd_json=1"
```

## Alternative Solutions

Beyond the [Web Scraper APIs](https://brightdata.com/products/web-scraper), Bright Data also provides ready-to-use [datasets](https://brightdata.com/products/datasets) tailored to travel industry needs:

- [Hotel Datasets](https://brightdata.com/products/datasets/travel/hotels)
- [Airbnb Dataset](https://brightdata.com/products/datasets/airbnb)
- [Expedia Datasets](https://brightdata.com/products/datasets/travel/expedia)
- [Tourism Datasets](https://brightdata.com/products/datasets/tourism)
- [Booking.com Datasets](https://brightdata.com/products/datasets/booking)
- [TripAdvisor Datasets](https://brightdata.com/products/datasets/tripadvisor)


## Support & Resources

- **Documentation**: [SERP API Docs](https://docs.brightdata.com/scraping-automation/serp-api/)
- **Explore Related Guides**: 
  - [Web Unlocker API](https://github.com/luminati-io/web-unlocker-api)
  - [SERP API](https://github.com/luminati-io/serp-api)
  - [Google Search API](https://github.com/luminati-io/google-search-api)
  - [Google News Scraper](https://github.com/luminati-io/Google-News-Scraper)
  - [Google Trends API](https://github.com/luminati-io/google-trends-api)
  - [Google Reviews API](https://github.com/luminati-io/google-reviews-api)
- **Helpful Articles**:
  - [Best SERP APIs](https://brightdata.com/blog/web-data/best-serp-apis)
  - [Build a RAG Chatbot with SERP API](https://brightdata.com/blog/web-data/build-a-rag-chatbot)
- **Use Cases**:
	- [SEO Applications](https://brightdata.com/use-cases/serp-tracking)
	- [Travel Industry Uses](https://brightdata.com/use-cases/travel)
- **Contact**: Need help? Email us at support@brightdata.com
