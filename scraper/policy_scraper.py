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
url = 'https://centraltickets.co.uk/privacy'
output_filename = 'data/policy.csv'

def policy_scrape():
    print("Setting up Chrome driver...")
    
    # Setup Chrome options for headless browsing
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    try:
        # Initialize Driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception as e:
        print(f"Error initializing Chrome driver. Details: {e}")
        return

    try:
        driver.get(url)
        print("Page loaded. Waiting for Privacy Policy content to render...")
        
        # 1. Wait until the main policy container is present (20 seconds)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "terms_web"))
        )
        # 2. Add an explicit wait for full rendering
        time.sleep(2) 
        
        print("Content detected. Extracting HTML...")

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        policy_data = []

        # Target the main container
        terms_container = soup.find('div', class_='terms_web')

        if terms_container:
            # --- FIX: Targeting the correct main list ID for the Privacy Policy ---
            main_ol = terms_container.find('ol', id='privacy_policy_section')
            
            if main_ol:
                # Get all direct children LIs (these are the main section wrappers, e.g., Who Are We?)
                sections = main_ol.find_all('li', recursive=False)

                for section in sections:
                    section_title = "N/A"
                    
                    # The title is usually in the first <span> child
                    title_tag = section.find('span', recursive=False)
                    if title_tag:
                        section_title = title_tag.get_text(strip=True)
                    
                    # Handle the "Last updated" date separately
                    if section_title.startswith("Last updated"):
                        policy_data.append(["Policy Update Date", section_title])
                        continue
                        
                    # Find all clause/content elements: nested <ol>, <p>, or <ul>
                    # We are looking for children of the section <li>, excluding the title span
                    content_elements = section.find_all(['ol', 'ul', 'p'], recursive=False)

                    # Also handle the initial clauses that are often nested immediately inside the first <ol>
                    if section.get('id') == 'privacy_policy_header':
                        content_elements.extend(section.find_all('ol', recursive=False))


                    for element in content_elements:
                        if element.name in ['ol', 'ul']:
                            # This handles lists of clauses or bullet points (including deeply nested ones)
                            
                            # Get all list items in this element, but stop at the first level of LI children
                            # This ensures we treat sub-bullets as part of the main clause content.
                            clauses = element.find_all('li', recursive=False)
                            
                            for clause in clauses:
                                # get_text with a space separator handles complex HTML inside the list item (b, a tags)
                                clause_text = clause.get_text(" ", strip=True)

                                # If it's an unordered list (ul), add a bullet marker for clarity in CSV
                                if element.name == 'ul':
                                    clause_text = "• " + clause_text
                                    
                                policy_data.append([section_title, clause_text])
                            
                        elif element.name == 'p':
                            # Handle paragraphs (e.g., introductory text in How We Use Your Information)
                            paragraph_text = element.get_text(" ", strip=True)
                            paragraph_text.replace('•','')
                            paragraph_text.strip()
                            if paragraph_text:
                                policy_data.append([section_title, paragraph_text])
            
            # 3. Write the data to CSV
            if policy_data:
                with open(output_filename, 'w', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(['Section', 'Clause Content'])
                    writer.writerows(policy_data)
                
                print(f"Successfully scraped {len(policy_data)} clauses to {output_filename}")
            else:
                print("Scraping failed: No policy clauses were found after parsing the loaded HTML. The selectors need review.")
        else:
            print("Error: The main 'terms_web' container was not found.")

    finally:
        # 4. Always close the browser
        driver.quit()

if __name__ == "__main__":
    policy_scrape()