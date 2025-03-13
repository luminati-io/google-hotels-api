import os
import time
import argparse
import tqdm
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def scrape_hotels(location_name="New York", max_hotels=None):
    """
    Scrape hotel data from Google Hotels.

    Args:
        location_name (str): Location to search for hotels.
        max_hotels (int, optional): Maximum number of hotels to scrape. If None, scrape all.
    """
    output_path = os.path.join(os.getcwd(), "hotels_data.csv")

    # Set up Selenium WebDriver with optimizations
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-extensions")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.set_page_load_timeout(30)

    base_url = f"https://www.google.com/travel/search?q={location_name}"

    if os.path.exists(output_path):
        os.remove(output_path)

    try:
        driver.get(base_url)
    except TimeoutException:
        print("Page load timed out, retrying...")
        driver.refresh()

    # Accept cookies if present
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(@aria-label, "Accept")]')
            )
        ).click()
    except (NoSuchElementException, TimeoutException):
        pass

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "K1smNd"))
        )
    except TimeoutException:
        print("Warning: Timed out waiting for hotel listings, continuing...")

    hotel_data = []
    unique_hotels = set()
    no_of_pages = 0
    hotels_scraped = 0
    next_button_clickable = True

    print(f"Scraping hotels in {location_name}...")

    pbar = (
        tqdm.tqdm(total=max_hotels, desc="Hotels scraped", unit="hotel")
        if max_hotels
        else None
    )

    def extract_hotel_details(hotel_item):
        """Extract basic hotel details from a hotel card."""
        try:
            name = (
                hotel_item.find("h2", class_="BgYkof").text
                if hotel_item.find("h2", class_="BgYkof")
                else "N/A"
            )
            price = (
                hotel_item.find("span", class_="qQOQpe prxS3d").text
                if hotel_item.find("span", class_="qQOQpe prxS3d")
                else "N/A"
            )
            rating = (
                hotel_item.find("span", class_="KFi5wf lA0BZ").text
                if hotel_item.find("span", class_="KFi5wf lA0BZ")
                else "N/A"
            )
            reviews_elem = hotel_item.find("span", class_="jdzyld XLC8M")
            reviews = reviews_elem.text.strip("() ") if reviews_elem else "N/A"
            hotel_link = hotel_item.find("a", class_="PVOOXe").get("href")
            return {
                "name": name,
                "price": price,
                "rating": rating,
                "reviews": reviews,
                "link": hotel_link,
            }
        except Exception as e:
            print(f"Error extracting details: {str(e)}")
            return None

    while next_button_clickable:
        soup = BeautifulSoup(driver.page_source, "lxml")
        hotel_cards = soup.find_all("div", class_="BcKagd")

        for hotel in hotel_cards:
            if max_hotels and hotels_scraped >= max_hotels:
                break

            hotel_info = extract_hotel_details(hotel)
            if not hotel_info:
                continue

            try:
                driver.get("https://www.google.com" + hotel_info["link"])
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "gJGKuf"))
                )

                location = (
                    driver.find_element(By.XPATH, '//div[@class="K4nuhf"]/span[1]').text
                    if driver.find_elements(By.XPATH, '//div[@class="K4nuhf"]/span[1]')
                    else "N/A"
                )
                contact = (
                    driver.find_element(By.XPATH, '//div[@class="K4nuhf"]/span[3]').text
                    if driver.find_elements(By.XPATH, '//div[@class="K4nuhf"]/span[3]')
                    else "N/A"
                )

                hotel_id = (
                    hotel_info["name"],
                    hotel_info["price"],
                    hotel_info["rating"],
                    hotel_info["reviews"],
                    location,
                    contact,
                )

                if hotel_id not in unique_hotels:
                    unique_hotels.add(hotel_id)
                    hotel_data.append(
                        {
                            "Name": hotel_info["name"],
                            "Price": hotel_info["price"],
                            "Rating": hotel_info["rating"],
                            "Reviews": hotel_info["reviews"],
                            "Location": location,
                            "Contact": contact,
                            "Link": "https://www.google.com" + hotel_info["link"],
                        }
                    )
                    hotels_scraped += 1

                    if pbar:
                        pbar.update(1)
                        pbar.set_postfix_str(f"Last: {hotel_info['name'][:20]}...")

                driver.execute_script("window.history.go(-1)")
                time.sleep(0.2)

            except Exception as e:
                print(f"Error processing hotel: {str(e)}")
                driver.execute_script("window.history.go(-1)")
                continue

        if max_hotels and hotels_scraped >= max_hotels:
            break

        if hotel_data:
            pd.DataFrame(hotel_data).to_csv(
                output_path,
                mode="a",
                header=not os.path.exists(output_path),
                index=False,
            )
            hotel_data.clear()

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "K1smNd"))
            )
            next_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        (
                            '//div[@class="eGUU7b"]/button'
                            if no_of_pages == 0
                            else '//div[@class="eGUU7b"]/button[2]'
                        ),
                    )
                )
            )
            next_button.click()
            no_of_pages += 1
            time.sleep(1.5)
        except (NoSuchElementException, TimeoutException):
            next_button_clickable = False

    if pbar:
        pbar.close()

    driver.quit()

    if hotel_data:
        pd.DataFrame(hotel_data).to_csv(
            output_path, mode="a", header=not os.path.exists(output_path), index=False
        )

    try:
        df = pd.read_csv(output_path)
        print(f"\nScraping complete! Collected data for {len(df)} hotels.")
        print(f"Data saved to {output_path}")
    except Exception as e:
        print(f"Error reading final CSV: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape hotel data from Google Hotels")
    parser.add_argument(
        "--location", type=str, default="New York", help="Location to search for hotels"
    )
    parser.add_argument(
        "--max_hotels",
        type=int,
        default=None,
        help="Maximum number of hotels to scrape",
    )

    args = parser.parse_args()

    try:
        scrape_hotels(args.location, args.max_hotels)
    except Exception as e:
        print(f"An error occurred: {str(e)}")