# Added essential comments, along with try except, and refined the code you provided.

import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# URL to scrape
URL = "https://centraltickets.co.uk/faq"
OUTPUT_FILE = "data\\faqs.csv"

def scrape_live_website():
    print("Setting up the browser...")
    
    # Setup Chrome Options (Headless mode to run without opening a visible window)
    # added more arguments.
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    # Add a user agent to look like a real user
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print(f"Loading {URL}...")
        driver.get(URL)

        # WAIT for the 'accordion-item' class to appear. 
        # This ensures the JavaScript has finished loading the questions.
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "accordion-item"))
            )
            print("Page loaded and JavaScript executed.")
        except Exception:
            print("Timeout: Content didn't load in time. The site structure might have changed.")
            return

        # Get the fully rendered HTML
        page_source = driver.page_source
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Extract FAQs
        accordion_items = soup.find_all('div', class_='accordion-item')
        extracted_data = []

        print(f"Found {len(accordion_items)} FAQ items. Extracting data...")

        for item in accordion_items:
            # Extract Question
            question_tag = item.find('span', class_='btn__text')
            question = question_tag.get_text(strip=True) if question_tag else "N/A"

            # Extract Answer
            answer_div = item.find('div', class_='accordion-body')
            if answer_div:
                answer = answer_div.get_text(separator="\n", strip=True)
            else:
                answer = "N/A"

            extracted_data.append([question, answer])

        # Save to CSV
        if extracted_data:
            with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Question', 'Answer'])
                writer.writerows(extracted_data)
            print(f"Success! Scraped {len(extracted_data)} FAQs and saved to '{OUTPUT_FILE}'")
        else:
            print("No data found. The website class names might have changed.")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_live_website()