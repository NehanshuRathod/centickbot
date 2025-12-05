import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Configuration
url = 'https://centraltickets.co.uk/terms'
output_filename = 'data/tnc.csv'

def scrape_live_tnc():
    print("Setting up Chrome driver...")
    
    # Setup Chrome options for headless browsing (runs in background)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    try:
        # Initialize Driver using webdriver_manager
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception as e:
        print(f"Error initializing Chrome driver. Details: {e}")
        return

    try:
        driver.get(url)
        print("Page loaded. Waiting for Terms & Conditions content to render...")
        
        # 1. Wait until the main T&C container is present (up to 15 seconds)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "terms_web"))
        )
        
        print("Content detected. Extracting HTML...")

        # 2. Get the HTML of the entire page after JavaScript has executed
        html_content = driver.page_source
        
        # 3. Use BeautifulSoup to parse the fully loaded content
        soup = BeautifulSoup(html_content, 'html.parser')
        tnc_data = []

        # Target the main container
        terms_container = soup.find('div', class_='terms_web')

        if terms_container:
            # The T&C sections are wrapped inside a specific nested list structure
            header_li = terms_container.find('li', id='terms_conditions_header')
            
            if header_li:
                sections_ol = header_li.find('ol')
                # Get all direct children LIs (these are the main sections like "Introduction")
                sections = sections_ol.find_all('li', recursive=False)

                for section in sections:
                    # --- Get Section Title ---
                    title_span = section.find('span')
                    section_title = title_span.get_text(strip=True) if title_span else "Unknown Section"

                    # --- Get Paragraphs (Clauses) ---
                    paragraphs_ol = section.find('ol')
                    
                    if paragraphs_ol:
                        paragraphs = paragraphs_ol.find_all('li', recursive=False)
                        
                        for p in paragraphs:
                            # The main clause text
                            text_span = p.find('span')
                            paragraph_text = text_span.get_text(" ", strip=True) if text_span else ""

                            # --- Check for nested bullet points (ul/li) ---
                            nested_ul = p.find('ul')
                            if nested_ul:
                                bullets = nested_ul.find_all('li')
                                bullet_texts = []
                                for b in bullets:
                                    b_text = b.get_text(" ", strip=True)
                                    bullet_texts.append(f"• {b_text}")
                                
                                # Append bullet points to the paragraph text, separated by a newline
                                if bullet_texts:
                                    paragraph_text += "\n\n" + "\n".join(bullet_texts)

                            if paragraph_text:
                                tnc_data.append([section_title, paragraph_text])

            
            # 4. Write the data to CSV
            if tnc_data:
                with open(output_filename, 'w', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    # Header: Section (the main heading) and Clause Content (the actual terms)
                    writer.writerow(['Section', 'Clause Content'])
                    writer.writerows(tnc_data)
                
                print(f"Successfully scraped {len(tnc_data)} clauses to {output_filename}")
            else:
                print("Scraping failed: No clauses were found after loading the page.")
        else:
            print("Error: The main 'terms_web' container was not found.")

    finally:
        # 5. Always close the browser
        driver.quit()

if __name__ == "__main__":
    scrape_live_tnc()