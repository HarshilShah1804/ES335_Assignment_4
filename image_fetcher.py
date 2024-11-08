# Horse vs Panda
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

chrome_driver_path = "../ChromeDriver/chromedriver-win64/chromedriver.exe" 
# Set up Chrome WebDriver
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(chrome_driver_path)  # Replace with your ChromeDriver path
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Search and download images
def download_images(search_query, num_images=5, save_folder='downloads'):
    # Create directory if it doesn't exist
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Initialize WebDriver
    driver = setup_driver()
    search_url = f"https://www.google.com/search?q={search_query}&tbm=isch"
    driver.get(search_url)
    print(f"Searching for images: {search_query}")

    # Scroll down to load more images
    for _ in range(10):  # Try scrolling more times if needed
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2)

    # Get image URLs using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    img_tags = soup.find_all("img", {"class": "YQ4gaf"}, limit=num_images)
    print(f"Found {len(img_tags)} image tags")

    img_urls = []
    for img in img_tags:
        try:
            img_url = img['src'] if 'src' in img.attrs else img['data-src']
            # Only include URLs that start with 'http' to avoid data URLs
            if img_url and img_url.startswith("http"):
                img_urls.append(img_url)
            else:
                print(f"Skipped non-http URL: {img_url}")
        except KeyError:
            print("Image tag missing 'src' or 'data-src' attribute")

    # Download images
    for i, img_url in enumerate(img_urls):
        try:
            print(f"Downloading image {i+1} from {img_url}")
            img_data = requests.get(img_url).content
            img = Image.open(BytesIO(img_data))
            if not os.path.exists(f"{save_folder}/{search_query}"):
                os.makedirs(f"{save_folder}/{search_query}")
            img_path = os.path.join(f"{save_folder}/{search_query}", f"{search_query}_{i+1}.jpg")
            img.save(img_path)
            print(f"Downloaded {img_path}")
            if len(os.listdir(os.path.join(f"downloads/{search_query}"))) == 300:
                break
        except Exception as e:
            print(f"Could not download image {i+1}: {e}")

    driver.quit()


# Example usage
download_images("panda", num_images=5000)
download_images("horse", num_images=5000)
